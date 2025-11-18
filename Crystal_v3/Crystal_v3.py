# -*- coding: utf-8 -*-
import sys, subprocess, os, time, tkinter as tk
from tkinter import messagebox, ttk
import locale, json, math, shutil, socket, ctypes, threading, queue
from pathlib import Path
from collections import deque, Counter
from typing import List, Dict, Optional, Set, Tuple
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def get_language():
    default_locale = locale.getdefaultlocale()[0]
    return 'ja' if default_locale and default_locale.startswith('ja') else 'en'

i18n = {
    'ja': {'title': "Crystal v3.1 (自動インストール)", 'gui_title': "Crystal v3.1", 'status_stopped': "ステータス: 停止中", 'status_running': "ステータス: 監視中", 'mode_sim': "シミュレーションモード (検知のみ)", 'mode_active': "アクティブ", 'btn_start': "監視開始", 'btn_stop': "監視停止", 'btn_whitelist': "ホワイトリスト編集", 'msg_config_reload': "設定再読み込み完了", 'msg_mode_change': "モード変更: ", 'lbl_config': "設定 & 操作", 'lbl_log': "リアルタイムログ", 'lbl_score': "リスクスコア: ", 'msg_admin_error': "管理者権限が必要です", 'install_title': "初回セットアップ", 'install_window': "インストール中...", 'install_progress': "必要な機能をダウンロード中...\nしばらくお待ちください。", 'install_success': "インストールが完了しました。\nアプリを起動します。", 'install_error': "インストールに失敗しました。\nインターネット接続を確認してください。", 'install_missing_lib': "Crystalの実行に必要なライブラリが見つかりません:\n{}\n\n今すぐ自動的にインストールしますか？\n(「はい」を押すとインストールが始まり、完了後にアプリが起動します)", 'install_exit': "終了", 'install_exit_msg': "ライブラリがないため終了します。", 'whitelist_desc': "左側のリストから信頼するアプリ(実行中)を選び、右側に追加してください。", 'whitelist_running': "現在実行中のプロセス (検出)", 'whitelist_add': "追加 >>", 'whitelist_remove': "<< 削除", 'whitelist_rescan': "更新 (再スキャン)", 'whitelist_list': "ホワイトリスト (除外対象)", 'whitelist_save': "設定を保存して閉じる"},
    'en': {'title': "Crystal v3.1 (Auto-Install)", 'gui_title': "Crystal v3.1", 'status_stopped': "Status: Stopped", 'status_running': "Status: Monitoring", 'mode_sim': "Simulation Mode (Detect Only)", 'mode_active': "Active", 'btn_start': "Start Monitoring", 'btn_stop': "Stop Monitoring", 'btn_whitelist': "Edit Whitelist", 'msg_config_reload': "Configuration Reloaded", 'msg_mode_change': "Mode Change: ", 'lbl_config': "Configuration & Control", 'lbl_log': "Real-time Log", 'lbl_score': "Risk Score: ", 'msg_admin_error': "Administrator privileges required", 'install_title': "Initial Setup", 'install_window': "Installing...", 'install_progress': "Downloading necessary dependencies...\nPlease wait.", 'install_success': "Installation complete.\nStarting the application.", 'install_error': "Installation failed.\nPlease check your internet connection.", 'install_missing_lib': "Required libraries for Crystal are missing:\n{}\n\nDo you want to install them automatically now?\n(Click 'Yes' to start installation and launch the app upon completion)", 'install_exit': "Exit", 'install_exit_msg': "Exiting due to missing libraries.", 'whitelist_desc': "Select trusted apps (running) from the left and add them to the right.", 'whitelist_running': "Running Processes (Detection)", 'whitelist_add': "Add >>", 'whitelist_remove': "<< Remove", 'whitelist_rescan': "Refresh (Rescan)", 'whitelist_list': "Whitelist (Exclusions)", 'whitelist_save': "Save Settings and Close"}
}

BASE = Path(__file__).resolve().parent
CFG_PATH = BASE / "config_v3.json"
DEFAULTS = {"dry_run": True, "watch_dirs": [r"%USERPROFILE%\\Documents", r"%USERPROFILE%\\Desktop"], "exclude_paths": [r"%WINDIR%", r"%ProgramFiles%", r"%ProgramFiles(x86)%"], "sus_exts": [".locked", ".encrypted", ".enc", ".crypt", ".crypted", ".akira"], "skip_entropy_exts": [".zip", ".7z", ".rar", ".jpg", ".png", ".mp4", ".avi", ".mp3", ".pdf", ".docx", ".xlsx", ".pptx"], "whitelist_processes": ["chrome.exe", "firefox.exe", "code.exe", "excel.exe", "winword.exe", "explorer.exe", "spotify.exe", "discord.exe", "teams.exe"], "canary_count_per_dir": 2, "entropy_window_sec": 10, "write_rate_mb_s_threshold": 20.0, "process_kill_mb_s_limit": 50.0, "rename_burst_threshold": 5, "entropy_jump_files": 3, "trip_score_threshold": 60, "post_trip_score_reset": 30, "isolate_dir": r"%USERPROFILE%\\Crystal_plus\\isolate", "logfile": r"%USERPROFILE%\\Crystal_plus\\crystal_v3.log", "honey_ports": [44555], "registry_poll_sec": 15, "registry_watch": ["HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"], "language": "auto"}

def expand_env(p: str): return os.path.expandvars(p)
def ensure_config():
    if not CFG_PATH.exists():
        with open(CFG_PATH, "w", encoding="utf-8") as f: json.dump(DEFAULTS, f, indent=2, ensure_ascii=False)

def load_cfg():
    with open(CFG_PATH, "r", encoding="utf-8") as f: user_cfg = json.load(f)
    cfg = DEFAULTS.copy(); cfg.update(user_cfg)
    for k in ("watch_dirs", "exclude_paths"): cfg[k] = [expand_env(x) for x in cfg.get(k, [])]
    for k in ("isolate_dir", "logfile"): cfg[k] = expand_env(cfg.get(k, ""))
    cfg["sus_exts_set"] = set(x.lower() for x in cfg["sus_exts"])
    cfg["skip_entropy_set"] = set(x.lower() for x in cfg["skip_entropy_exts"])
    cfg["whitelist_set"] = set(x.lower() for x in cfg["whitelist_processes"])
    if cfg["language"] == "auto": cfg["current_lang"] = get_language()
    else: cfg["current_lang"] = cfg["language"]
    global T
    T = i18n[cfg["current_lang"]]
    return cfg

def save_cfg(cfg_data):
    clean_data = cfg_data.copy()
    for k in ["sus_exts_set", "skip_entropy_set", "whitelist_set", "current_lang"]:
        if k in clean_data: del clean_data[k]
    clean_data["whitelist_processes"] = sorted(list(set(clean_data["whitelist_processes"])))
    with open(CFG_PATH, "w", encoding="utf-8") as f: json.dump(clean_data, f, indent=2, ensure_ascii=False)

def install_dependencies_and_restart(missing_packages):
    root = tk.Tk(); root.withdraw()
    msg = T['install_missing_lib'].format(', '.join(missing_packages))
    if not messagebox.askyesno(T['install_title'], msg):
        messagebox.showwarning(T['install_exit'], T['install_exit_msg']); sys.exit()
    install_win = tk.Toplevel(root); install_win.title(T['install_window']); install_win.geometry("350x100")
    lbl = tk.Label(install_win, text=T['install_progress'], pady=20); lbl.pack(); root.update()
    pip_packages = []
    for pkg in missing_packages: pip_packages.append("pywin32") if pkg == "win32api" else pip_packages.append(pkg)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + pip_packages)
        messagebox.showinfo(T['install_success'], T['install_success'])
        python = sys.executable; os.execl(python, python, *sys.argv)
    except subprocess.CalledProcessError:
        messagebox.showerror(T['install_error'], T['install_error']); sys.exit()

def check_requirements():
    missing = []
    try: import watchdog
    except ImportError: missing.append("watchdog")
    try: import psutil
    except ImportError: missing.append("psutil")
    try: import win32api
    except ImportError: missing.append("win32api")
    if missing: install_dependencies_and_restart(missing)

class BasiliskCore:
    def __init__(self, cfg: dict):
        self.update_config(cfg); self.q_events = queue.Queue(); self.write_sizes = deque(); self.rename_burst = deque()
        self.entropy_hits = deque(); self.sus_ext_hits = deque(); self.score = 0; self.lock = threading.Lock()
        self.canary_paths: List[str] = []; self.pid_stats: Dict[int, Tuple[float, int]] = {}; self.pid_suspect_cache = set()
        self.RUNNING = False; self.obs: Optional[Observer] = None; self.threads: List[threading.Thread] = []; self.honey_sockets: List[socket.socket] = []
    def update_config(self, cfg):
        self.cfg = cfg; self.DRY_RUN = cfg["dry_run"]; self.WATCH_DIRS = cfg["watch_dirs"]; self.EXCLUDE = [p.rstrip("\\/") for p in cfg["exclude_paths"]]
        self.SUS_EXTS = cfg["sus_exts_set"]; self.SKIP_ENTROPY = cfg["skip_entropy_set"]; self.WHITELIST = cfg["whitelist_set"]
        self.CANARY_PER_DIR = int(cfg["canary_count_per_dir"]); self.ENTROPY_WINDOW_SEC = int(cfg["entropy_window_sec"]); self.WRITE_RATE_THRESHOLD = float(cfg["write_rate_mb_s_threshold"])
        self.PROCESS_KILL_LIMIT = float(cfg["process_kill_mb_s_limit"]); self.RENAME_BURST_THRESHOLD = int(cfg["rename_burst_threshold"]); self.ENTROPY_JUMP_FILES = int(cfg["entropy_jump_files"])
        self.TRIP_SCORE_THRESHOLD = int(cfg["trip_score_threshold"]); self.POST_TRIP_RESET = int(cfg["post_trip_score_reset"]); self.ISOLATE_DIR = Path(cfg["isolate_dir"])
        self.LOGFILE = Path(cfg["logfile"]); self.HONEY_PORTS = list(cfg.get("honey_ports", [])); self.REG_POLL_SEC = int(cfg.get("registry_poll_sec", 15)); self.REG_WATCH_KEYS = list(cfg.get("registry_watch", []))
    def now(self): return time.time()
    def is_excluded(self, path: str) -> bool:
        up = path.upper()
        for e in self.EXCLUDE:
            if up.startswith(e.upper()): return True
        return False
    def file_entropy(self, path: str, max_bytes=64*1024) -> float:
        try:
            p = Path(path)
            if p.suffix.lower() in self.SKIP_ENTROPY: return 0.0
            with open(path, "rb") as f: data = f.read(max_bytes)
            if not data: return 0.0
            c = Counter(data); l = len(data)
            return -sum((n/l)*math.log2(n/l) for n in c.values())
        except Exception: return 0.0
    def log_event(self, obj: Dict):
        try:
            self.LOGFILE.parent.mkdir(parents=True, exist_ok=True)
            log_entry = {"t": int(self.now()), "dry_run": self.DRY_RUN, **obj}
            print(f"{'[SIM]' if self.DRY_RUN else '[ACT]'} {obj.get('level','INFO')}: {obj}")
            with open(self.LOGFILE, "a", encoding="utf-8") as f: f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except: pass
    def log_exception(self, context, e): self.log_event({"level":"error", "action": context, "error": str(e)})
    def run_cmd(self, cmd: str):
        if self.DRY_RUN: self.log_event({"level":"info", "action":"simulated_cmd", "cmd": cmd}); return
        try: subprocess.run(cmd, capture_output=True, text=True, shell=True)
        except Exception as e: self.log_exception('run_cmd', e)
    def firewall_block_all(self): self.run_cmd('netsh advfirewall set allprofiles firewallpolicy blockinbound,blockoutbound')
    def disconnect_netdrives(self): self.run_cmd('net use * /delete /y')
    def vss_snapshot(self):
        if not self.DRY_RUN: self.run_cmd('vssadmin create shadow /for=C:')
    def kill_suspects_smart(self):
        current_time = self.now(); victims = []
        for p in psutil.process_iter(["pid", "name", "io_counters"]):
            try:
                pid = p.info["pid"]; name = (p.info["name"] or "").lower()
                if name in ("system", "registry", "smss.exe", "csrss.exe", "wininit.exe", "services.exe", "lsass.exe"): continue
                if name in self.WHITELIST: continue
                io = p.info.get("io_counters");
                if not io: continue
                current_bytes = io.write_bytes
                prev_t, prev_bytes = self.pid_stats.get(pid, (0, 0)); self.pid_stats[pid] = (current_time, current_bytes)
                if prev_t == 0: continue
                dt = current_time - prev_t
                if dt < 0.5: continue
                diff_mb = (current_bytes - prev_bytes) / (1024 * 1024); rate_mb_s = diff_mb / dt
                if rate_mb_s > self.PROCESS_KILL_LIMIT and pid not in self.pid_suspect_cache: victims.append((p, rate_mb_s))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): continue
            except Exception: pass
        for p, rate in victims:
            try:
                msg = f"Process {p.name()} (PID: {p.pid}) writing at {rate:.1f} MB/s"
                if self.DRY_RUN: self.log_event({"level":"warn", "action":"SIMULATED_KILL", "msg": msg})
                else: self.log_event({"level":"warn", "action":"KILLING", "msg": msg}); p.kill(); self.pid_suspect_cache.add(p.pid)
            except Exception as e: self.log_exception('kill_fail', e)
        if len(self.pid_stats) > 1000: self.pid_stats.clear()
    def safe_isolate(self, path: str):
        if self.DRY_RUN: return
        try:
            p = Path(path);
            if not p.exists(): return
            self.ISOLATE_DIR.mkdir(parents=True, exist_ok=True)
            dest = self.ISOLATE_DIR / f"{int(time.time())}_{p.name}"; shutil.copy2(str(p), str(dest))
        except Exception as e: self.log_exception('isolate', e)
    def place_canaries(self):
        if self.DRY_RUN: return
        import random, string
        for d in self.WATCH_DIRS:
            pd = Path(d);
            if not pd.exists(): continue
            for _ in range(self.CANARY_PER_DIR):
                name = ".~$" + "".join(random.choices(string.ascii_letters, k=8)) + ".docx"; cp = pd / name
                if not cp.exists():
                    try:
                        with open(cp, "wb") as f: f.write(os.urandom(4096))
                        self.canary_paths.append(str(cp)); ctypes.windll.kernel32.SetFileAttributesW(str(cp), 0x02)
                    except: pass
    class Handler(FileSystemEventHandler):
        def __init__(self, core): self.core = core
        def on_any_event(self, event):
            if event.is_directory: return
            path = event.src_path if hasattr(event, "src_path") else getattr(event, "dest_path", "")
            if not path or self.core.is_excluded(path): return
            try: sz = os.path.getsize(path) if os.path.exists(path) else 0
            except: sz = 0
            kind = event.event_type
            if kind == "moved": path = getattr(event, "dest_path", path)
            self.core.q_events.put((kind, path, sz))
    def score_update(self, delta: int, reason: str):
        with self.lock: self.score = max(0, self.score + delta)
        if delta > 5: self.log_event({"level":"info", "score_up": delta, "reason": reason, "total": self.score})
    def scorer_thread(self):
        while self.RUNNING:
            self.kill_suspects_smart()
            try:
                while True:
                    evt, path, sz = self.q_events.get_nowait(); t = self.now(); ext = Path(path).suffix.lower()
                    if path in self.canary_paths and evt in ("modified", "moved", "deleted"):
                        self.score_update(100, "CANARY_TRIP"); self.log_event({"level":"trip", "msg": f"Canary accessed: {path}"})
                    if evt in ("created", "moved") and ext in self.SUS_EXTS:
                        self.sus_ext_hits.append(t); self.score_update(10, f"SUS_EXT: {ext}")
                    if evt == "moved":
                        self.rename_burst.append(t)
                        if len(self.rename_burst) > self.RENAME_BURST_THRESHOLD: self.score_update(2, "RENAME_BURST")
                    if evt in ("modified", "created") and sz > 1024 and sz < 10*1024*1024:
                        if ext not in self.SKIP_ENTROPY:
                            if self.file_entropy(path) > 7.8:
                                self.entropy_hits.append(t); self.score_update(5, "HIGH_ENTROPY"); self.safe_isolate(path)
                    if evt in ("created", "modified"): self.write_sizes.append((t, sz))
            except queue.Empty: pass
            t0 = self.now()
            for d in (self.write_sizes, self.rename_burst, self.entropy_hits, self.sus_ext_hits):
                while d and (t0 - (d[0][0] if isinstance(d[0], tuple) else d[0]) > self.ENTROPY_WINDOW_SEC): d.popleft()
            if self.write_sizes:
                mb_s = (sum(b for _, b in self.write_sizes) / (1024*1024)) / self.ENTROPY_WINDOW_SEC
                if mb_s > self.WRITE_RATE_THRESHOLD: self.score_update(1, "HIGH_GLOBAL_WRITE")
            with self.lock: current_score = self.score
            if current_score >= self.TRIP_SCORE_THRESHOLD:
                self.log_event({"level":"trip", "trip": True, "score": current_score})
                if not self.DRY_RUN:
                    for f in (self.firewall_block_all, self.disconnect_netdrives, self.vss_snapshot): threading.Thread(target=f).start()
                with self.lock: self.score = self.POST_TRIP_RESET
                time.sleep(5)
            time.sleep(0.5)
    def registry_thread(self):
        import winreg
        def snap(keys):
            res = {}
            for k in keys:
                try:
                    hive_str, sub = k.split("\\", 1); h = getattr(winreg, hive_str)
                    with winreg.OpenKey(h, sub) as key:
                        i = 0; vals = []
                        while True:
                            try: vals.append(str(winreg.EnumValue(key, i))); i+=1
                            except OSError: break
                        res[k] = sorted(vals)
                except Exception: pass
            return res
        prev = snap(self.REG_WATCH_KEYS)
        while self.RUNNING:
            time.sleep(self.REG_POLL_SEC)
            cur = snap(self.REG_WATCH_KEYS)
            if cur != prev: self.log_event({"level":"warn", "msg": "Registry Changed"}); self.score_update(10, "REGISTRY_CHANGE"); prev = cur
    def honey_listener(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind(("0.0.0.0", port)); s.listen(5); self.honey_sockets.append(s)
            while self.RUNNING:
                try: s.settimeout(1); c, a = s.accept(); self.log_event({"level":"trip", "honey_hit": port}); self.score_update(50, "HONEYPOT_HIT"); c.close()
                except: pass
        except: pass
        finally: s.close()
    def start(self):
        if self.RUNNING: return
        self.RUNNING = True; self.place_canaries(); self.obs = Observer(); h = BasiliskCore.Handler(self)
        for d in self.WATCH_DIRS:
            if Path(d).exists(): self.obs.schedule(h, d, recursive=True)
        self.obs.start()
        self.threads = [threading.Thread(target=self.scorer_thread, daemon=True), threading.Thread(target=self.registry_thread, daemon=True)]
        for p in self.HONEY_PORTS: self.threads.append(threading.Thread(target=self.honey_listener, args=(p,), daemon=True))
        for t in self.threads: t.start()
        return True
    def stop(self):
        self.RUNNING = False
        if self.obs: self.obs.stop(); self.obs.join()
        for s in self.honey_sockets:
            try: s.close()
            except: pass

class WhitelistWindow(tk.Toplevel):
    def __init__(self, parent, cfg):
        super().__init__(parent); self.title(T['btn_whitelist']); self.geometry("700x500"); self.cfg = cfg; self.parent = parent
        ttk.Label(self, text=T['whitelist_desc'], padding=10).pack()
        frm = ttk.Frame(self, padding=10); frm.pack(fill="both", expand=True)
        lf = ttk.LabelFrame(frm, text=T['whitelist_running']); lf.pack(side="left", fill="both", expand=True, padx=5)
        self.lb_running = tk.Listbox(lf, selectmode="multiple", exportselection=False); scroll_l = ttk.Scrollbar(lf, orient="vertical", command=self.lb_running.yview)
        self.lb_running.config(yscrollcommand=scroll_l.set); self.lb_running.pack(side="left", fill="both", expand=True); scroll_l.pack(side="right", fill="y")
        cf = ttk.Frame(frm); cf.pack(side="left", padx=5)
        ttk.Button(cf, text=T['whitelist_add'], command=self.add_to_whitelist).pack(pady=5); ttk.Button(cf, text=T['whitelist_remove'], command=self.remove_from_whitelist).pack(pady=5)
        ttk.Button(cf, text=T['whitelist_rescan'], command=self.scan_processes).pack(pady=20)
        rf = ttk.LabelFrame(frm, text=T['whitelist_list']); rf.pack(side="left", fill="both", expand=True, padx=5)
        self.lb_white = tk.Listbox(rf, selectmode="multiple", exportselection=False); scroll_r = ttk.Scrollbar(rf, orient="vertical", command=self.lb_white.yview)
        self.lb_white.config(yscrollcommand=scroll_r.set); self.lb_white.pack(side="left", fill="both", expand=True); scroll_r.pack(side="right", fill="y")
        ttk.Button(self, text=T['whitelist_save'], command=self.save_and_close).pack(pady=10)
        self.scan_processes(); self.load_current_whitelist()
    def scan_processes(self):
        self.lb_running.delete(0, "end"); procs = set()
        for p in psutil.process_iter(['name']):
            try: procs.add(p.info['name'].lower()) if p.info['name'] else None
            except: pass
        for name in sorted(list(procs)): self.lb_running.insert("end", name)
    def load_current_whitelist(self):
        self.lb_white.delete(0, "end")
        for name in sorted(self.cfg.get("whitelist_processes", [])): self.lb_white.insert("end", name)
    def add_to_whitelist(self):
        for i in self.lb_running.curselection():
            val = self.lb_running.get(i)
            if val not in self.lb_white.get(0, "end"): self.lb_white.insert("end", val)
    def remove_from_whitelist(self):
        for i in reversed(self.lb_white.curselection()): self.lb_white.delete(i)
    def save_and_close(self):
        self.cfg["whitelist_processes"] = list(self.lb_white.get(0, "end")); save_cfg(self.cfg); self.parent.reload_config(); self.destroy()

class App(tk.Tk):
    def __init__(self):
        super().__init__(); ensure_config(); self.cfg = load_cfg()
        self.current_lang = self.cfg["current_lang"]
        self.T = i18n[self.current_lang]
        self.core = BasiliskCore(self.cfg)
        self.title(self.T['title']); self.geometry("600x500"); self.resizable(False, False)
        frame = ttk.Frame(self, padding=10); frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=self.T['gui_title'], font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ctrl_frame = ttk.LabelFrame(frame, text=self.T['lbl_config'], padding=10); ctrl_frame.pack(fill="x", pady=10)
        self.dry_run_var = tk.BooleanVar(value=self.core.DRY_RUN)
        self.chk_dry = ttk.Checkbutton(ctrl_frame, text=self.T['mode_sim'], variable=self.dry_run_var, command=self.update_mode); self.chk_dry.pack(anchor="w")
        btn_row = ttk.Frame(ctrl_frame); btn_row.pack(fill="x", pady=10)
        self.btn_start = ttk.Button(btn_row, text=self.T['btn_start'], command=self.toggle_start); self.btn_start.pack(side="left", padx=5)
        ttk.Button(btn_row, text=self.T['btn_whitelist'], command=self.open_whitelist).pack(side="left", padx=5)
        lang_text = "言語: 日本語" if self.current_lang == 'ja' else "Language: English"
        self.btn_lang = ttk.Button(btn_row, text=lang_text, command=self.toggle_language); self.btn_lang.pack(side="left", padx=5)
        self.status_var = tk.StringVar(value=self.T['status_stopped'])
        ttk.Label(ctrl_frame, textvariable=self.status_var).pack(anchor="w", pady=5)
        mon_frame = ttk.LabelFrame(frame, text=self.T['lbl_log'], padding=10); mon_frame.pack(fill="both", expand=True)
        self.score_var = tk.StringVar(value=f"{self.T['lbl_score']}0")
        ttk.Label(mon_frame, textvariable=self.score_var).pack(anchor="w")
        self.log_text = tk.Text(mon_frame, height=12, state="disabled", font=("Consolas", 9)); self.log_text.pack(fill="both", expand=True, pady=5)
        self.after(1000, self.update_ui)

    def reload_config(self):
        self.cfg = load_cfg(); self.core.update_config(self.cfg); self.log_msg(self.T['msg_config_reload'])
    def open_whitelist(self): WhitelistWindow(self, self.cfg)
    def update_mode(self):
        self.core.DRY_RUN = self.dry_run_var.get(); mode_text = self.T['mode_sim'] if self.core.DRY_RUN else self.T['mode_active']
        self.log_msg(f"{self.T['msg_mode_change']}{mode_text}")
    def toggle_start(self):
        if not self.core.RUNNING:
            if not ctypes.windll.shell32.IsUserAnAdmin(): messagebox.showerror(self.T['msg_admin_error'], self.T['msg_admin_error']); return
            self.core.DRY_RUN = self.dry_run_var.get(); self.core.start()
            self.btn_start.configure(text=self.T['btn_stop']); self.status_var.set(self.T['status_running'])
        else:
            self.core.stop(); self.btn_start.configure(text=self.T['btn_start']); self.status_var.set(self.T['status_stopped'])
    
    def toggle_language(self):
        global T
        new_lang = 'en' if self.current_lang == 'ja' else 'ja'
        self.cfg['language'] = new_lang
        self.cfg['current_lang'] = new_lang
        save_cfg(self.cfg)
        self.current_lang = new_lang
        self.T = i18n[new_lang]
        T = self.T
        self.update_gui_text()
        self.log_msg(self.T['msg_config_reload'])

    def update_gui_text(self):
        self.title(self.T['title'])
        self.children['!frame'].children['!label'].config(text=self.T['gui_title'])
        self.children['!frame'].children['!labelframe'].config(text=self.T['lbl_config'])
        self.chk_dry.config(text=self.T['mode_sim'])
        btn_text = self.T['btn_stop'] if self.core.RUNNING else self.T['btn_start']
        self.btn_start.config(text=btn_text)
        self.children['!frame'].children['!labelframe'].children['!frame'].children['!button2'].config(text=self.T['btn_whitelist'])
        lang_text = "言語: 日本語" if self.current_lang == 'ja' else "Language: English"
        self.btn_lang.config(text=lang_text)
        status_text = self.T['status_running'] if self.core.RUNNING else self.T['status_stopped']
        self.status_var.set(status_text)
        self.children['!frame'].children['!labelframe2'].config(text=self.T['lbl_log'])
        score_val = self.score_var.get().split('/')
        score_num = score_val[0].split(':')[-1].strip() if ':' in score_val[0] else '0'
        self.score_var.set(f"{self.T['lbl_score']}{score_num} / {self.core.TRIP_SCORE_THRESHOLD}")
        self.log_msg(f"{self.T['msg_mode_change']}{self.T['mode_sim'] if self.core.DRY_RUN else self.T['mode_active']}")

    def log_msg(self, msg):
        self.log_text.configure(state="normal"); self.log_text.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see("end"); self.log_text.configure(state="disabled")
    def update_ui(self):
        if self.core.RUNNING: self.score_var.set(f"{self.T['lbl_score']}{self.core.score} / {self.core.TRIP_SCORE_THRESHOLD}")
        self.after(1000, self.update_ui)

ensure_config(); load_cfg(); check_requirements()

if __name__ == "__main__":
    app = App()
    app.mainloop()