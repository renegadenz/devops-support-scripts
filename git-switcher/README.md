# Git Profile Switcher

This script allows you to switch between Git profiles using a selectable menu.

## Requirements

- Bash shell
- Git

## Usage

1. Clone the `devops-support-scripts` repository to your local machine:
```
git clone https://github.com/renegadenz/devops-support-scripts.git
```
2. Change to the `git-switcher` subdirectory:
```
cd devops-support-scripts/git-switcher
```

3. Modify the `profiles_dir` and `profiles` variables in the `switch-profiles.sh` script to match the location and names of your Git profiles.

4. Make the script executable by running the following command:
```
chmod +x switch-profiles.sh
```

5. (Optional) If you want to use the script with an alias in your `~/.bashrc` file, open the file in a text editor:
```
nano ~/.bashrc
```

6. Add the following line to the end of the file:
```
alias git-profile='~/path/to/devops-support-scripts/git-switcher/switch-profiles.sh
```

Replace `~/path/to` with the actual path to the `devops-support-scripts` repository on your system.

7. Save and close the `~/.bashrc` file.

8. Reload the `~/.bashrc` file by running the following command:

```
source ~/.bashrc
```

9. To switch between Git profiles, run the following command:
```
git-profile
```

This will run the `switch-profiles.sh` script from the `git-switcher` subdirectory of the `devops-support-scripts` repository and display a selectable menu of your Git profiles in the terminal. Use the arrow keys to select the profile you want to switch to and press Enter.

10. The script will switch to the selected Git profile and print a message confirming the switch.

## Troubleshooting

- If the script is not finding your Git profiles, make sure they are saved in the directory specified by the `profiles_dir` variable and with the names specified in the `profiles` array.

- If you're having issues with the script using an alias in your `~/.bashrc` file, try running the script directly from the terminal using the instructions in the previous section.







