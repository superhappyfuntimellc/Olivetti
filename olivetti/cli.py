#!/usr/bin/env python3
"""Command-line interface for Olivetti writing assistant."""

import sys
import argparse
from pathlib import Path
from typing import Optional

from olivetti import WritingAssistant, VoiceProfile
from olivetti.config import Config


def cmd_continue(args):
    """Continue writing command."""
    assistant = WritingAssistant(voice_profile=args.profile)
    
    # Read text from stdin or file
    if args.file:
        with open(args.file, 'r') as f:
            text = f.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print("Please provide text via stdin or --file")
        return 1
    
    result = assistant.continue_writing(text, args.length)
    print(result)
    return 0


def cmd_rewrite(args):
    """Rewrite text command."""
    assistant = WritingAssistant(voice_profile=args.profile)
    
    # Read text from stdin or file
    if args.file:
        with open(args.file, 'r') as f:
            text = f.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print("Please provide text via stdin or --file")
        return 1
    
    result = assistant.rewrite(text, args.instruction or "")
    print(result)
    return 0


def cmd_describe(args):
    """Describe subject command."""
    assistant = WritingAssistant(voice_profile=args.profile)
    
    result = assistant.describe(args.subject, args.detail)
    result = assistant.describe(args.subject, args.detail_level)
    print(result)
    return 0


def cmd_brainstorm(args):
    """Brainstorm ideas command."""
    assistant = WritingAssistant(voice_profile=args.profile)
    
    result = assistant.brainstorm(args.topic, args.count)
    print(result)
    return 0


def cmd_dialogue(args):
    """Generate dialogue command."""
    assistant = WritingAssistant(voice_profile=args.profile)
    
    characters = [c.strip() for c in args.characters.split(',')]
    result = assistant.dialogue(characters, args.situation, args.length)
    print(result)
    return 0


def cmd_analyze(args):
    """Analyze text command."""
    assistant = WritingAssistant(voice_profile=args.profile)
    
    # Read text from stdin or file
    if args.file:
        with open(args.file, 'r') as f:
            text = f.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print("Please provide text via stdin or --file")
        return 1
    
    result = assistant.analyze(text)
    print(result)
    return 0


def cmd_profile_create(args):
    """Create voice profile command."""
    profile = VoiceProfile(args.name)
    
    if args.style:
        profile.set_style_notes(args.style)
    
    if args.genre:
        for genre in args.genre:
            profile.add_genre_preference(genre)
    
    profile.save()
    print(f"Created voice profile: {args.name}")
    return 0


def cmd_profile_list(args):
    """List voice profiles command."""
    profiles = VoiceProfile.list_profiles()
    
    if not profiles:
        print("No voice profiles found.")
    else:
        print("Available voice profiles:")
        for profile in profiles:
            print(f"  - {profile}")
    
    return 0


def cmd_profile_delete(args):
    """Delete voice profile command."""
    if VoiceProfile.delete_profile(args.name):
        print(f"Deleted voice profile: {args.name}")
        return 0
    else:
        print(f"Profile not found: {args.name}")
        return 1


def cmd_profile_add_sample(args):
    """Add writing sample to profile."""
    profile = VoiceProfile(args.profile)
    
    # Read sample from stdin or file
    if args.file:
        with open(args.file, 'r') as f:
            text = f.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print("Please provide text via stdin or --file")
        return 1
    
    profile.add_writing_sample(text, args.description or "")
    print(f"Added writing sample to profile: {args.profile}")
    return 0


def cmd_config(args):
    """Configure Olivetti."""
    config = Config()
    
    if args.set:
        key, value = args.set.split('=', 1)
        config.set(key, value)
        print(f"Set {key} = {value}")
    
    elif args.get:
        value = config.get(args.get)
        print(f"{args.get} = {value}")
    
    elif args.list:
        print("Current configuration:")
        for key in ["api_provider", "model", "temperature", "max_tokens", "default_voice_profile"]:
            value = config.get(key)
            print(f"  {key} = {value}")
    
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Olivetti - Personal AI writing assistant for novelists",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Continue writing
  echo "The old house stood..." | olivetti continue
  olivetti continue --file chapter.txt --length long
  
  # Rewrite text
  echo "He walked slowly" | olivetti rewrite --instruction "more dramatic"
  
  # Describe something
  olivetti describe "a mysterious forest clearing" --detail extensive
  
  # Brainstorm ideas
  olivetti brainstorm "plot twists for mystery novel" --count 10
  
  # Generate dialogue
  olivetti dialogue --characters "Alice, Bob" --situation "confronting a betrayal"
  
  # Create voice profile
  olivetti profile create my-voice --style "literary fiction, introspective"
  olivetti profile add-sample my-voice --file my-writing.txt
  
  # Configure
  olivetti config --set api_provider=openai
  olivetti config --set model=gpt-4
  olivetti config --set default_voice_profile=my-voice
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Continue command
    continue_parser = subparsers.add_parser('continue', help='Continue writing from text')
    continue_parser.add_argument('--file', '-f', help='Read text from file')
    continue_parser.add_argument('--length', '-l', choices=['short', 'medium', 'long'], 
                                default='medium', help='Length of continuation')
    continue_parser.add_argument('--profile', '-p', help='Voice profile to use')
    continue_parser.set_defaults(func=cmd_continue)
    
    # Rewrite command
    rewrite_parser = subparsers.add_parser('rewrite', help='Rewrite text')
    rewrite_parser.add_argument('--file', '-f', help='Read text from file')
    rewrite_parser.add_argument('--instruction', '-i', help='How to rewrite')
    rewrite_parser.add_argument('--profile', '-p', help='Voice profile to use')
    rewrite_parser.set_defaults(func=cmd_rewrite)
    
    # Describe command
    describe_parser = subparsers.add_parser('describe', help='Describe a subject')
    describe_parser.add_argument('subject', help='What to describe')
    describe_parser.add_argument('--detail', '-d', choices=['brief', 'detailed', 'extensive'],
    describe_parser.add_argument('--detail-level', '-d', choices=['brief', 'detailed', 'extensive'],
                                default='detailed', help='Level of detail')
    describe_parser.add_argument('--profile', '-p', help='Voice profile to use')
    describe_parser.set_defaults(func=cmd_describe)
    
    # Brainstorm command
    brainstorm_parser = subparsers.add_parser('brainstorm', help='Brainstorm ideas')
    brainstorm_parser.add_argument('topic', help='Topic to brainstorm about')
    brainstorm_parser.add_argument('--count', '-c', type=int, default=5, 
                                  help='Number of ideas')
    brainstorm_parser.add_argument('--profile', '-p', help='Voice profile to use')
    brainstorm_parser.set_defaults(func=cmd_brainstorm)
    
    # Dialogue command
    dialogue_parser = subparsers.add_parser('dialogue', help='Generate dialogue')
    dialogue_parser.add_argument('--characters', '-c', required=True,
                               help='Comma-separated character names')
    dialogue_parser.add_argument('--situation', '-s', required=True,
                               help='Situation/context for dialogue')
    dialogue_parser.add_argument('--length', '-l', choices=['short', 'medium', 'long'],
                               default='medium', help='Length of dialogue')
    dialogue_parser.add_argument('--profile', '-p', help='Voice profile to use')
    dialogue_parser.set_defaults(func=cmd_dialogue)
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze text')
    analyze_parser.add_argument('--file', '-f', help='Read text from file')
    analyze_parser.add_argument('--profile', '-p', help='Voice profile to use')
    analyze_parser.set_defaults(func=cmd_analyze)
    
    # Profile commands
    profile_parser = subparsers.add_parser('profile', help='Manage voice profiles')
    profile_subparsers = profile_parser.add_subparsers(dest='profile_command')
    
    # Profile create
    profile_create = profile_subparsers.add_parser('create', help='Create voice profile')
    profile_create.add_argument('name', help='Profile name')
    profile_create.add_argument('--style', '-s', help='Style notes')
    profile_create.add_argument('--genre', '-g', action='append', help='Genre preference')
    profile_create.set_defaults(func=cmd_profile_create)
    
    # Profile list
    profile_list = profile_subparsers.add_parser('list', help='List voice profiles')
    profile_list.set_defaults(func=cmd_profile_list)
    
    # Profile delete
    profile_delete = profile_subparsers.add_parser('delete', help='Delete voice profile')
    profile_delete.add_argument('name', help='Profile name')
    profile_delete.set_defaults(func=cmd_profile_delete)
    
    # Profile add sample
    profile_add_sample = profile_subparsers.add_parser('add-sample', 
                                                       help='Add writing sample to profile')
    profile_add_sample.add_argument('profile', help='Profile name')
    profile_add_sample.add_argument('--file', '-f', help='Read sample from file')
    profile_add_sample.add_argument('--description', '-d', help='Sample description')
    profile_add_sample.set_defaults(func=cmd_profile_add_sample)
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Configure Olivetti')
    config_parser.add_argument('--set', help='Set config value (key=value)')
    config_parser.add_argument('--get', help='Get config value')
    config_parser.add_argument('--list', action='store_true', help='List all config values')
    config_parser.set_defaults(func=cmd_config)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        return args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
