import os
import webbrowser
import subprocess
import platform
import datetime
import pyautogui
import shutil
import psutil
from dateutil import parser

# === Access Modes ===
safe_mode = True          # 🟢 Default: Safe-only
advanced_mode = False     # 🟡 Manual toggle
admin_mode = False        # 🔴 Locked behind secret

# === App Aliases ===
app_aliases = {
    "browser": "chrome",
    "editor": "code",
    "notes": "notepad",
    "terminal": "cmd"
}

def run_system_task(intent, params=None):
    global safe_mode, advanced_mode, admin_mode

    if params is None:
        params = {}

    try:
        intent = intent.strip().lower()
        print(f"🔧 Received intent: {intent}, params: {params}")

        # === Allow Mode Unlocks First ===
        if intent == "enable_advanced":
            advanced_mode = True
            return "🟡 Advanced Mode enabled."
        elif intent == "enable_admin":
            admin_mode = True
            return "🔴 Admin Mode enabled."
            
        # === Admin Mode Restrictions ===
        admin_only = ["run_shell", "delete_file", "rename_file", "shutdown", "restart_system"]
        if intent in admin_only and not admin_mode:
            return f"🔴 '{intent}' is locked under Admin Mode."
        
        # === Advanced Mode Restrictions ===
        advanced_only = ["clean_downloads", "move_files", "system_report", "clean_by_date"]
        if intent in advanced_only and not advanced_mode:
            return f"🟡 '{intent}' requires Advanced Mode. Use enable_advanced first."
        
        # === Safe Mode Restrictions ===
        safe_allowed = [
            "open_notepad", "open_calculator", "open_browser", "take_screenshot",
            "get_time_date_status", "count_files", "open_app", "search_google"
        ]
        if intent not in safe_allowed and not advanced_mode and not  admin_mode:
            return f"🔒 '{intent}' is not allowed."

        # === Task Execution ===
        match intent:
            case "open_notepad": return open_application("notepad")
            case "open_calculator": return open_application("calc")
            case "open_browser": return open_application("chrome")
            case "take_screenshot": return take_screenshot()
            case "get_time_date_status": return get_time_date_battery()
            case "count_files":
                folder = params.get("folder", os.getcwd())
                return count_files_in_folder(folder)
            case "search_google":
                query = params.get("query", "latest news")
                return search_google(query)
            case "shutdown": return shutdown_system()
            case "restart_system": return restart_system()
            case "open_app":
                app = params.get("app", "")
                return open_application_by_alias(app)
            case "run_shell":
                cmd = params.get("cmd", "")
                return run_shell_command(cmd)
            case "delete_file":
                path = params.get("path", "")
                return delete_file(path)
            case "rename_file":
                src = params.get("src", "")
                dest = params.get("dest", "")
                return rename_file(src, dest)
            case "clean_downloads": return clean_downloads()
            case "move_files":
                filetype = params.get("type", "pdf")
                dest = params.get("dest", os.path.expanduser("~/Documents"))
                return move_files_by_type(filetype, dest)
            case "create_folder":
                location = params.get("location", os.path.expanduser("~/Documents"))
                name = params.get("name", "NewFolder")
                return create_folder(location, name)
            case "system_report": return get_system_report()
            case "clean_by_date":
                date = params.get("date", "")
                filter = params.get("filter", "before")
                return clean_downloads_by_date(filter, date)
            case _:
                return f"⚠️ Unknown system intent: '{intent}'"

    except Exception as e:
        return f"❌ System task failed: {str(e)}"

# === Task Functions ===

def open_application_by_alias(user_input):
    app = app_aliases.get(user_input.lower(), user_input)
    return open_application(app)

def open_application(app_name):
    try:
        system = platform.system()
        if system == "Windows":
            os.system(f"start {app_name}")
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", app_name])
        elif system == "Linux":
            app_path = shutil.which(app_name)
            if app_path:
                subprocess.Popen([app_path])
            else:
                return f"❌ Application '{app_name}' not found in PATH."
        return f"✅ Opening application: {app_name}"
    except Exception as e:
        return f"❌ Failed to open '{app_name}': {str(e)}"

def take_screenshot():
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{now}.png"
    pyautogui.screenshot().save(filename)
    return f"📸 Screenshot saved as {filename}"

def get_time_date_battery():
    now = datetime.datetime.now().strftime("%A, %d %B %Y %I:%M %p")
    battery_status = "Battery info not available."
    try:
        battery = psutil.sensors_battery()
        if battery:
            battery_status = f"{battery.percent}% {'(Plugged in)' if battery.power_plugged else '(On battery)'}"
    except:
        pass
    return f"🕒 Time: {now} | 🔋 Battery: {battery_status}"

def count_files_in_folder(folder_path):
    try:
        count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        return f"📁 {count} files in: '{folder_path}'"
    except Exception as e:
        return f"❌ Error counting files: {e}"

def search_google(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"🔍 Searching Google for: {query}"

def shutdown_system():
    if platform.system() == "Windows":
        os.system("shutdown /s /t 10")
    else:
        os.system("shutdown -h now")
    return "⚠️ System shutting down in 10 seconds."

def restart_system():
    if platform.system() == "Windows":
        os.system("shutdown /r /t 5")
    else:
        os.system("shutdown -r now")
    return "🔁 Restarting system..."

def run_shell_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return f"💻 Shell Output:\n{output}"
    except subprocess.CalledProcessError as e:
        return f"❌ Shell Error: {e.output}"

def delete_file(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
            return f"🗑️ Deleted: {path}"
        return f"❌ File not found: {path}"
    except Exception as e:
        return f"❌ Delete failed: {e}"

def rename_file(src, dest):
    try:
        if os.path.exists(src):
            os.rename(src, dest)
            return f"🖊️ Renamed to: {dest}"
        return f"❌ Source file not found: {src}"
    except Exception as e:
        return f"❌ Rename failed: {e}"

def clean_downloads():
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    deleted = []
    try:
        for f in os.listdir(downloads_path):
            f_path = os.path.join(downloads_path, f)
            if os.path.isfile(f_path):
                os.remove(f_path)
                deleted.append(f_path)
        if not deleted:
            return "🧹 No files to delete in Downloads."
        return f"🧹 Deleted {len(deleted)} files:\n" + "\n".join(deleted)
    except Exception as e:
        return f"❌ Failed to clean downloads: {e}"

def move_files_by_type(filetype, destination):
    source = os.path.join(os.path.expanduser("~"), "Downloads")
    if "desktop" in destination.lower():
        destination = os.path.join(os.path.expanduser("~"), "Desktop")
    elif "documents" in destination.lower():
        destination = os.path.join(os.path.expanduser("~"), "Documents")
    elif destination.lower() in ['d:', 'd']:
        destination = "D:/"
    elif not os.path.exists(destination):
        os.makedirs(destination)
    moved = 0
    final_paths = []
    try:
        for f in os.listdir(source):
            if f.lower().endswith(f".{filetype.lower()}"):
                src = os.path.join(source, f)
                dst = os.path.join(destination, f)
                shutil.move(src, dst)
                moved += 1
                final_paths.append(dst)
        return f"📦 Moved {moved} .{filetype} files to {destination}:\n" + "\n".join(final_paths)
    except Exception as e:
        return f"❌ Failed to move files: {e}"

def create_folder(location, name):
    try:
        if "desktop" in location.lower():
            location = os.path.join(os.path.expanduser("~"), "Desktop")
        elif "documents" in location.lower():
            location = os.path.join(os.path.expanduser("~"), "Documents")
        elif location.lower() in ['d:', 'd']:
            location = "D:/"
        path = os.path.join(location, name)
        os.makedirs(path, exist_ok=True)
        return f"📁 Folder created at: {path}"
    except Exception as e:
        return f"❌ Failed to create folder: {e}"

def get_system_report():
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        return (
            f"📊 System Report:\n"
            f"CPU: {cpu}%\n"
            f"RAM: {ram.percent}% of {round(ram.total / (1024 ** 3), 2)} GB\n"
            f"Disk: {disk.percent}% of {round(disk.total / (1024 ** 3), 2)} GB"
        )
    except Exception as e:
        return f"❌ Failed to generate report: {e}"

def clean_downloads_by_date(filter='on', date_str='2024-01-01'):
    try:
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        target_date = parser.parse(date_str).date()
        deleted_files = []
        for f in os.listdir(downloads_path):
            f_path = os.path.join(downloads_path, f)
            if not os.path.isfile(f_path): continue
            file_time = datetime.date.fromtimestamp(os.path.getmtime(f_path))
            if ((filter == "before" and file_time < target_date) or
                (filter == "on" and file_time == target_date) or
                (filter == "after" and file_time > target_date)):
                os.remove(f_path)
                deleted_files.append(f_path)
        if not deleted_files:
            return f"🧹 No files matched filter='{filter}' and date='{target_date}'"
        return f"🧹 Deleted {len(deleted_files)} files:\n" + "\n".join(deleted_files)
    except Exception as e:
        return f"❌ Failed to clean by date: {e}"

# === Manual Test Loop ===
if __name__ == "__main__":
    print("🧪 Type system intent (e.g., open_app app=chrome | clean_by_date filter=before date=2024-07-01)")
    while True:
        user_input = input(">> ")
        if user_input.lower() == "exit":
            break
        try:
            parts = user_input.strip().split()
            intent = parts[0]
            params = {k: v for k, v in (p.split('=') for p in parts[1:])}
        except:
            print("⚠️ Format: intent param=value")
            continue
        print(run_system_task(intent, params))
