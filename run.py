"""
Starting point of the application. This module is invoked from
the command line to run the analyses.
"""

import argparse

# Import each feature script as a module
import scripts.label_count as label_count
import scripts.resolution_time as resolution_time
import scripts.user_issues as user_issues

def parse_args():
    ap = argparse.ArgumentParser("run.py")
    ap.add_argument('--feature', '-f', type=int, required=True,
                    help='Which of the three features to run: 1 (label count), 2 (resolution time), 3 (user participation)')
    return ap.parse_args()

def main():
    args = parse_args()

    if args.feature == 1:
        print("Running Feature 1: Label Count Analysis")
        label_count.run()
    elif args.feature == 2:
        print("Running Feature 2: Resolution Time Analysis")
        resolution_time.run()
    elif args.feature == 3:
        print("Running Feature 3: User Participation Analysis")
        user_issues.run()
    else:
        print("Invalid feature selected. Choose 1, 2, or 3.")

if __name__ == "__main__":
    main()

