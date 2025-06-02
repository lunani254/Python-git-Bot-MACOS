#!/usr/bin/env python3
"""
macOS-specific utilities for the Git Auto-Pusher
"""

import subprocess
import keyring

try:
    from Foundation import NSUserNotification, NSUserNotificationCenter
    FOUNDATION_AVAILABLE = True
except ImportError:
    FOUNDATION_AVAILABLE = False
    print("Warning: Foundation framework not available. Notifications will use fallback method.")


def send_notification(title, message):
    """Send macOS notification using the best available method"""
    if FOUNDATION_AVAILABLE:
        try:
            # Use Foundation framework for native notifications
            notification = NSUserNotification.alloc().init()
            notification.setTitle_(title)
            notification.setInformativeText_(message)
            NSUserNotificationCenter.defaultUserNotificationCenter(
            ).deliverNotification_(notification)
            return True
        except Exception as e:
            print(f"Foundation notification failed: {e}")

    # Fallback to osascript (AppleScript)
    try:
        script = f'''
        display notification "{message}" with title "{title}"
        '''
        subprocess.run(['osascript', '-e', script],
                       check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"AppleScript notification failed: {e}")
        return False
    except Exception as e:
        print(f"Notification error: {e}")
        return False


def get_credentials():
    """Retrieve GitHub credentials from Keychain"""
    try:
        username = keyring.get_password('github-username', 'git-auto-pusher')
        token = keyring.get_password('github-token', 'git-auto-pusher')

        # Return None if either is empty string or None
        if not username or not token:
            return None, None

        return username, token
    except Exception as e:
        print(f"Error retrieving credentials: {e}")
        return None, None


def set_credentials(username, token):
    """Store GitHub credentials in Keychain"""
    try:
        keyring.set_password('github-username', 'git-auto-pusher', username)
        keyring.set_password('github-token', 'git-auto-pusher', token)
        return True
    except Exception as e:
        print(f"Error storing credentials: {e}")
        return False


def clear_credentials():
    """Clear stored GitHub credentials from Keychain"""
    try:
        keyring.delete_password('github-username', 'git-auto-pusher')
        keyring.delete_password('github-token', 'git-auto-pusher')
        return True
    except Exception as e:
        print(f"Error clearing credentials: {e}")
        return False


def test_keychain_access():
    """Test if keychain access is working"""
    try:
        test_key = 'git-auto-pusher-test'
        test_value = 'test-value'

        # Try to set and get a test value
        keyring.set_password('test', test_key, test_value)
        retrieved = keyring.get_password('test', test_key)

        # Clean up
        keyring.delete_password('test', test_key)

        return retrieved == test_value
    except Exception as e:
        print(f"Keychain test failed: {e}")
        return False


def get_macos_version():
    """Get macOS version information"""
    try:
        result = subprocess.run(['sw_vers', '-productVersion'],
                                capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error getting macOS version: {e}")
        return None


if __name__ == "__main__":
    # Test the utilities
    print("Testing macOS utilities...")

    print(f"Foundation available: {FOUNDATION_AVAILABLE}")
    print(f"macOS version: {get_macos_version()}")
    print(f"Keychain access: {test_keychain_access()}")

    # Test notification
    send_notification("Test", "Git Auto-Pusher utilities test")
    print("Test notification sent")
