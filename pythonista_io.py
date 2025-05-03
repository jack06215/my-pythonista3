import editor
import clipboard
import platform
import console
from objc_util import ObjCClass

def get_feedback_generator(style=4):
    """
    style: 0 (light), 1 (medium), 2 (heavy), 3 (soft), 4 (rigid)
    Returns a UIImpactFeedbackGenerator if supported, else None.
    """
    try:
        device = platform.machine()
        # iPad or simulator (x86_64/arm64)
        if device.startswith("iPad") or device in ("x86_64", "arm64"):
            return None

        UIImpactFeedbackGenerator = ObjCClass('UIImpactFeedbackGenerator')
        generator = UIImpactFeedbackGenerator.alloc().initWithStyle_(style)
        generator.prepare()
        return generator
    except Exception:
        return None

def fallback_alert(msg="Haptic feedback not supported."):
    console.alert("Notice", msg, "OK", hide_cancel_button=True)

def main():
    feedback = get_feedback_generator(4)
    path = editor.get_path()

    if path:
        clipboard.set(path)
        print("Copied to clipboard:", path)
    else:
        print("No file open in editor.")

    if feedback:
        feedback.impactOccurred()
    else:
        fallback_alert()

if __name__ == '__main__':
    main()
