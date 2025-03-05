import os
import subprocess
import webbrowser
import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import time

# Get computer name & timestamp for unique file naming
def run_command(command):
    try:
        return subprocess.getoutput(command)
    except Exception as e:
        return f"Error running command: {str(e)}"

computer_name = run_command("hostname").strip()  # Get PC Name
timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")   # Get Current Time

# File paths (Ensures each report is unique)
TXT_FILE = f"C:\\system_info_{computer_name}_{timestamp}.txt"
PDF_FILE = f"C:\\system_info_{computer_name}_{timestamp}.pdf"
BATTERY_REPORT = f"C:\\battery_report_{computer_name}_{timestamp}.html"

# Function to check if a battery is present
def is_battery_available():
    check_battery = run_command("wmic path Win32_Battery get BatteryStatus")
    return "BatteryStatus" in check_battery and "1" in check_battery  # BatteryStatus=1 means battery exists

# Function to generate battery report (Only if a battery exists)
def generate_battery_report():
    if is_battery_available():
        try:
            subprocess.run(["powercfg", "/batteryreport", "/output", BATTERY_REPORT], shell=True)
            return f"Battery report saved: {BATTERY_REPORT}\n"
        except Exception as e:
            return f"Error generating battery report: {str(e)}\n"
    else:
        return "No battery detected. Battery report not generated.\n"

# Function to generate system report
def generate_report():
    try:
        with open(TXT_FILE, "w") as f:
            f.write("=== System Information ===\n")
            f.write(run_command("systeminfo | findstr /B /C:\"OS Name\" /C:\"OS Version\""))
            f.write("\n=== Computer Name ===\n")
            f.write(run_command("hostname"))
            f.write("\n=== Current User ===\n")
            f.write(run_command("whoami"))
            f.write("\n=== CPU Info ===\n")
            f.write(run_command("wmic cpu get name,NumberOfCores,NumberOfLogicalProcessors"))
            f.write("\n=== RAM Info (MB) ===\n")
            f.write(run_command("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value"))
            f.write("\n=== Disk Space (GB) ===\n")
            f.write(run_command("wmic logicaldisk get caption, size, freespace"))
            f.write("\n=== IP Configuration ===\n")
            f.write(run_command("ipconfig | findstr /C:\"IPv4\""))
            f.write("\n=== Active Network Connections ===\n")
            f.write(run_command("netstat -ano"))
            f.write("\n=== Installed Services ===\n")
            f.write(run_command("sc query type= service state= all"))

            # Battery Report Section
            f.write("\n=== Battery Report ===\n")
            battery_output = generate_battery_report()
            f.write(battery_output)

        # Convert text report to PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        with open(TXT_FILE, "r") as f:
            for line in f:
                pdf.cell(200, 10, txt=line, ln=True)
        pdf.output(PDF_FILE)

        messagebox.showinfo("Success", f"Reports saved:\n{TXT_FILE}\n{PDF_FILE}\n{BATTERY_REPORT if is_battery_available() else 'No Battery Report'}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

# Function to open Battery Report in Browser (Only if battery report exists)
def open_battery_report():
    if os.path.exists(BATTERY_REPORT) and is_battery_available():
        webbrowser.open(BATTERY_REPORT)
    else:
        messagebox.showerror("Error", "No battery detected. Battery report is not available.")

# GUI Design
root = tk.Tk()
root.title("System Info Tool")
root.geometry("400x300")

tk.Label(root, text="System Information Tool", font=("Arial", 14, "bold")).pack(pady=10)

btn_generate = tk.Button(root, text="Generate System Report", command=generate_report, width=25)
btn_generate.pack(pady=5)

btn_battery = tk.Button(root, text="Open Battery Report", command=open_battery_report, width=25)
btn_battery.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", command=root.quit, width=25)
btn_exit.pack(pady=5)

root.mainloop()
