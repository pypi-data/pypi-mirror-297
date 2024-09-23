import os
import requests
from datetime import datetime, timedelta

from rich import box
from rich.align import Align
from rich.console import Console

from rich.table import Table

from argparse import ArgumentParser

console = Console(record=True)

def fetch_and_parse_github_activities(url, headers, start_date=None, end_date=None):

    all_activities = []

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            console.print(f"[red]Error fetching data from GitHub API: {response.status_code}[/red]")
            break
        activities = response.json()

        early_stops = 0
        for activity in activities:
            try:
                dto = datetime.strptime(activity['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
                if (start_date and dto < start_date) or (end_date and dto > end_date + timedelta(days=1)):
                    if (start_date and dto < start_date):
                        early_stops += 1
                    continue  # 범위 밖이면 넘어가기
                
                datum = {
                    "branch": activity['ref'].replace('refs/heads/', ''),
                    "timestamp": f'{dto.year}/{dto.month}/{dto.day} {dto.hour}:{dto.minute}:{dto.second}',
                    "activity_type": activity["activity_type"],
                    "actor": activity["actor"]["login"],
                }
                all_activities.append(datum)
            except KeyError as e:
                console.print(f"[yellow]Missing key in activity data: {e}[/yellow]")
                continue

        if early_stops == len(activities):
            break
        # 다음 페이지로 이동 (pagination)
        url = response.links['next']['url'] if 'next' in response.links else None

        
    # 데이터 파싱 및 정렬
    activities = []
    for entry in all_activities:
        timestamp = datetime.strptime(entry['timestamp'], '%Y/%m/%d %H:%M:%S')
        activities.append((timestamp, entry['branch'], entry['activity_type'], entry['actor']))
    activities.sort(key=lambda x: x[0])  # 시간 순서대로 정렬

    return activities


def generate_workflow(activities, core_branches, team_info):
    
    # 테이블 생성 및 설정
    table = Table(show_footer=False, show_edge=False)
    table.box = box.SIMPLE
    table_centered = Align.center(table)

    colors = ["red", "green", "cyan", "magenta", "yellow", "purple", "white", "gold3", "orange3", "gray63" ]
    branch_columns = {}
    branch_status = {}
    actors = {}
    actor_colors = {}
    color_index = 0

    branch_name = 'time'
    table.add_column(branch_name, justify="center", no_wrap=True)
    branch_columns[branch_name] = len(branch_columns)

    branch_creations = []

    for timestamp, branch_name, activity, actor in activities:
        if activity == 'branch_creation':
            branch_creations.append(branch_name)
        
        if branch_name not in branch_columns:
            branch_columns[branch_name] = len(branch_columns)

        if actor not in actors:
            actors[actor] = True
            actor_colors[actor] = colors[color_index % len(colors)]
            color_index += 1

    actor_intro = ''.join(f' [{actor_colors[actor]}]󰙃 {actor}[/{actor_colors[actor]}]' for actor in actor_colors)
    table.title = f"[bold]{team_info['team']}[/bold]\n{actor_intro}"

    for branch_name in branch_columns:
        if branch_name == 'time':
            continue
        if branch_name in branch_creations:
            branch_status[branch_name] = False
        else:
            branch_status[branch_name] = True # 이미 있던 브랜치임 |    | 표시해야 됨
        
        if branch_name in core_branches:
            pass
        elif 'release' in branch_name.lower():
            branch_name = f'R{branch_columns[branch_name]}'
        elif 'hotfix' in branch_name.lower(): 
            branch_name = f'H{branch_columns[branch_name]}'
        else:
            branch_name = f'F{branch_columns[branch_name]}'
            
        table.add_column(branch_name, justify="center", no_wrap=True)

    last_row_data = [None] * len(branch_columns)
    last_timestamp_mmdd = None  # 이전 timestamp의 MMDD 값을 추적하는 변수

    for timestamp, branch_name, activity, actor in activities: 

        cell = {
            'branch_creation': f'┌─󱓊─┐',
            'branch_deletion': f'└─󱓋─┘',
            'force_push': f'│~~│' if branch_status[branch_name] else f'~~',
            'push': f'│  │' if branch_status[branch_name] else f'',
            'pr_merge': f'│  │',
        }.get(activity, f'󰀍')

        if activity == 'branch_creation':
            table.columns[branch_columns[branch_name]].header_style = 'not dim'
            branch_status[branch_name] = True
        elif activity == 'branch_deletion':
            table.columns[branch_columns[branch_name]].header_style = 'dim'
            branch_status[branch_name] = False

        timestamp_mmdd = timestamp.strftime("%m/%d")
        display_timestamp_mmdd = timestamp_mmdd if timestamp_mmdd != last_timestamp_mmdd else ""
        
        
        row_data = [display_timestamp_mmdd] + [None] * (len(branch_columns) - 1)  # 첫 열에 timestamp MMDD 추가

        for br in branch_status:
            if branch_status[br]:
                row_data[branch_columns[br]] = '│   │'

        row_data[branch_columns[branch_name]] = f'[{actor_colors[actor]}]{cell}[/{actor_colors[actor]}]'

        if row_data[1:] != last_row_data[1:]:  # 연속된 행을 방지
            table.add_row(*row_data)
            last_row_data = row_data.copy()
            last_timestamp_mmdd = timestamp_mmdd  # 이전 timestamp의 MMDD 값을 업데이트

    branches = ''.join(f'[b]#{branch_columns[branch]}:[/b] {branch}\n' for branch in branch_columns if branch != 'time')

    console.print(table)
    console.print('\n')
    console.print(branches)


def main():
    argparser = ArgumentParser(description="Visualize GitHub Repository Workflow Activities")
    argparser.add_argument('url', type=str, help="GitHub repository URL")
    argparser.add_argument('--core_branches', nargs='*', type=str, help="List of core branch names. Other branch names would be abstracted (release->R, hotfix->H, feature->F)", default=[])
    argparser.add_argument('--start_date', type=str, help="Start date in YYYY-MM-DD format", default=None)
    argparser.add_argument('--end_date', type=str, help="End date in YYYY-MM-DD format", default=None)
    argparser.add_argument('--token', type=str, help="GitHub API token", default=os.getenv("GITHUB_TOKEN"))

    args = argparser.parse_args()
    

    if not args.token:
        console.print("[red]GitHub API token is required. Please set GITHUB_TOKEN environment variable or use --token option.[/red]")
        exit(1)

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d") if args.start_date else None
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d") if args.end_date else None


    team_info = {
        'team': args.url.split('https://github.com/')[-1],
        'repo': args.url
    }


    core_branches = list(set(args.core_branches + ['main', 'master', 'develop', 'dev']))

    owner, repo = team_info['repo'].replace('https://github.com/', '').split('/')

# GitHub API Endpoint 설정
    URL = f"https://api.github.com/repos/{owner}/{repo}/activity"

    headers = {
        'Authorization': f'token {args.token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    activities = fetch_and_parse_github_activities(URL, headers, start_date, end_date)
    generate_workflow(activities, core_branches, team_info)

if __name__ == '__main__':
    main()