#!/usr/bin/env python3
"""
Test script to verify YouTube live video filtering functionality
"""

import sys
from pathlib import Path

# Add current directory to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from youtube_channel_transcriber import YouTubeChannelTranscriber
from rich.console import Console

console = Console()

def test_live_video_filtering():
    """Test the live video filtering functionality"""
    
    console.print("[cyan]Testing Live Video Filtering Logic[/cyan]")
    
    # Create mock video entries to test filtering
    mock_entries = [
        {
            'id': 'video1',
            'title': 'Regular Video 1',
            'upload_date': '20251015',
            'duration': 600,
            'was_live': False
        },
        {
            'id': 'video2', 
            'title': 'Live Stream 1',
            'upload_date': '20251016',
            'duration': 3600,
            'was_live': True
        },
        {
            'id': 'video3',
            'title': 'Live Stream 2', 
            'upload_date': '20251017',
            'duration': 7200,
            'was_live': True
        },
        {
            'id': 'video4',
            'title': 'Regular Video 2',
            'upload_date': '20251014',
            'duration': 900,
            'was_live': False
        },
        {
            'id': 'video5',
            'title': 'Current Live Stream',
            'upload_date': '20251017',
            'duration': 1800,
            'is_live': True
        }
    ]
    
    transcriber = YouTubeChannelTranscriber()
    
    # Test 1: Live videos only, no limit
    console.print("\n[yellow]Test 1: Live videos only (should be 3 videos, sorted by date)[/yellow]")
    filtered = transcriber.filter_videos(mock_entries, live_only=True)
    
    for i, video in enumerate(filtered):
        live_status = "LIVE" if video.get('was_live') or video.get('is_live') else "Regular"
        console.print(f"  {i+1}. {video['title']} ({video['upload_date']}) - {live_status}")
    
    expected_live_count = 3
    if len(filtered) == expected_live_count:
        console.print("[green]✓ PASS: Correct number of live videos filtered[/green]")
    else:
        console.print(f"[red]✗ FAIL: Expected {expected_live_count} live videos, got {len(filtered)}[/red]")
    
    # Check if sorted by date (most recent first)
    if len(filtered) >= 2:
        if filtered[0]['upload_date'] >= filtered[1]['upload_date']:
            console.print("[green]✓ PASS: Videos sorted by date (most recent first)[/green]")
        else:
            console.print("[red]✗ FAIL: Videos not properly sorted by date[/red]")
    
    # Test 2: All videos, with max limit
    console.print("\n[yellow]Test 2: All videos, max 3 videos (should prioritize live)[/yellow]")
    filtered = transcriber.filter_videos(mock_entries, max_videos=3, live_only=False)
    
    for i, video in enumerate(filtered):
        live_status = "LIVE" if video.get('was_live') or video.get('is_live') else "Regular"
        console.print(f"  {i+1}. {video['title']} ({video['upload_date']}) - {live_status}")
    
    if len(filtered) == 3:
        console.print("[green]✓ PASS: Correct number of videos with limit[/green]")
    else:
        console.print(f"[red]✗ FAIL: Expected 3 videos, got {len(filtered)}[/red]")
    
    # Test 3: Duration filtering
    console.print("\n[yellow]Test 3: Duration filter (max 30 minutes = 1800 seconds)[/yellow]")
    filtered = transcriber.filter_videos(mock_entries, duration_limit=30, live_only=False)
    
    for i, video in enumerate(filtered):
        live_status = "LIVE" if video.get('was_live') or video.get('is_live') else "Regular"
        duration_min = video['duration'] // 60
        console.print(f"  {i+1}. {video['title']} ({duration_min}min) - {live_status}")
    
    # Should filter out videos longer than 30 minutes (1800 seconds)
    long_videos = [v for v in filtered if v['duration'] > 1800]
    if len(long_videos) == 0:
        console.print("[green]✓ PASS: Duration filter working correctly[/green]")
    else:
        console.print(f"[red]✗ FAIL: Found {len(long_videos)} videos longer than limit[/red]")
    
    console.print("\n[cyan]Live Video Filtering Test Complete![/cyan]")

if __name__ == '__main__':
    test_live_video_filtering()