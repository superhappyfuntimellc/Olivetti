#!/usr/bin/env python3
"""
Example usage of Olivetti writing assistant.

This script demonstrates how to use Olivetti programmatically.
"""

from olivetti import WritingAssistant, VoiceProfile

def main():
    print("=== Olivetti Example Usage ===\n")
    
    # Create a voice profile
    print("1. Creating a voice profile...")
    profile = VoiceProfile("example-voice")
    
    # Set style preferences
    profile.set_style_notes(
        "Literary fiction with lyrical prose, focuses on character psychology "
        "and atmospheric descriptions. Prefers complex sentence structures "
        "and rich vocabulary."
    )
    
    # Add genre preferences
    profile.add_genre_preference("literary fiction")
    profile.add_genre_preference("psychological thriller")
    
    # Add a writing sample
    sample_text = """
    The rain had stopped, leaving the cobblestones slick and gleaming under 
    the streetlamps. Margaret stood at the corner, her coat drawn tight against 
    the autumn chill, watching the last of the evening commuters hurry past. 
    She had been standing there for twenty minutes, waiting for someone who 
    might never come, harboring hopes she knew were foolish.
    """
    
    profile.add_writing_sample(sample_text, "Opening scene from novel")
    profile.save()
    
    print(f"✓ Created profile: {profile.name}\n")
    
    # Initialize the assistant with this profile
    print("2. Initializing WritingAssistant...")
    assistant = WritingAssistant(voice_profile="example-voice")
    print("✓ Assistant ready\n")
    
    # Example text to work with
    starting_text = "The letter arrived on a Tuesday morning, unremarkable except for its timing."
    
    print("3. Example operations:\n")
    
    # Note: These will only work if you have an API key configured
    # Uncomment to test with a real API key
    
    print(f"Starting text: '{starting_text}'\n")
    
    # Example 1: Continue writing
    print("Example: assistant.continue_writing(text, 'short')")
    print("  (Would continue the narrative in your style)\n")
    
    # Example 2: Describe something
    print("Example: assistant.describe('a Victorian study room', 'detailed')")
    print("  (Would generate a vivid, style-matched description)\n")
    
    # Example 3: Brainstorm
    print("Example: assistant.brainstorm('plot twists involving mistaken identity', 5)")
    print("  (Would generate creative ideas in your genre)\n")
    
    # Example 4: Generate dialogue
    print("Example: assistant.dialogue(['Emma', 'James'], 'discussing a family secret')")
    print("  (Would generate natural dialogue in your style)\n")
    
    # List available profiles
    print("4. Available voice profiles:")
    profiles = VoiceProfile.list_profiles()
    for p in profiles:
        print(f"  - {p}")
    
    print("\n=== Example Complete ===")
    print("\nTo use with a real API key:")
    print("1. Set OPENAI_API_KEY environment variable")
    print("2. Uncomment the actual API calls in this script")
    print("3. Run: python examples/example_usage.py")


if __name__ == "__main__":
    main()
