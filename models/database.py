import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="social_media_analysis.db"):
        self.db_name = db_name
        self._create_tables()
        
    def _create_tables(self):
        """创建数据库表"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # 用户表
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 分析任务表
        c.execute('''
        CREATE TABLE IF NOT EXISTS analysis_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task_name TEXT NOT NULL,
            platform TEXT NOT NULL,
            analysis_type TEXT NOT NULL,
            data_source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        # 分析结果表
        c.execute('''
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            result_type TEXT NOT NULL,
            result_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES analysis_tasks (id)
        )
        ''')
        
        # 营销方案表
        c.execute('''
        CREATE TABLE IF NOT EXISTS marketing_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task_id INTEGER,
            plan_name TEXT NOT NULL,
            plan_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (task_id) REFERENCES analysis_tasks (id)
        )
        ''')
        
        # 数据导入表
        c.execute('''
        CREATE TABLE IF NOT EXISTS data_imports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            import_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            data_count INTEGER NOT NULL,
            platform TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        conn.commit()
        conn.close()
        
    def add_user(self, username, password, email):
        """添加新用户"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                      (username, password, email))
            conn.commit()
            user_id = c.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            return None
            
    def get_user(self, username, password=None):
        """获取用户信息"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        if password:
            c.execute("SELECT id, username, email FROM users WHERE username = ? AND password = ?", 
                      (username, password))
        else:
            c.execute("SELECT id, username, email FROM users WHERE username = ?", 
                      (username,))
        user = c.fetchone()
        conn.close()
        return user
        
    def add_analysis_task(self, user_id, task_name, platform, analysis_type, data_source=None):
        """添加分析任务"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO analysis_tasks (user_id, task_name, platform, analysis_type, data_source) VALUES (?, ?, ?, ?, ?)", 
                  (user_id, task_name, platform, analysis_type, data_source))
        conn.commit()
        task_id = c.lastrowid
        conn.close()
        return task_id
        
    def get_analysis_tasks(self, user_id):
        """获取用户的分析任务"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT id, task_name, platform, analysis_type, created_at FROM analysis_tasks WHERE user_id = ? ORDER BY created_at DESC", 
                  (user_id,))
        tasks = c.fetchall()
        conn.close()
        return tasks
        
    def add_analysis_result(self, task_id, result_type, result_data):
        """添加分析结果"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO analysis_results (task_id, result_type, result_data) VALUES (?, ?, ?)", 
                  (task_id, result_type, result_data))
        conn.commit()
        result_id = c.lastrowid
        conn.close()
        return result_id
        
    def get_analysis_results(self, task_id):
        """获取分析结果"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT id, result_type, result_data, created_at FROM analysis_results WHERE task_id = ? ORDER BY created_at DESC", 
                  (task_id,))
        results = c.fetchall()
        conn.close()
        return results
        
    def add_marketing_plan(self, user_id, task_id, plan_name, plan_data):
        """添加营销方案"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO marketing_plans (user_id, task_id, plan_name, plan_data) VALUES (?, ?, ?, ?)", 
                  (user_id, task_id, plan_name, plan_data))
        conn.commit()
        plan_id = c.lastrowid
        conn.close()
        return plan_id
        
    def get_marketing_plans(self, user_id):
        """获取用户的营销方案"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT mp.id, mp.plan_name, mp.created_at, at.task_name FROM marketing_plans mp LEFT JOIN analysis_tasks at ON mp.task_id = at.id WHERE mp.user_id = ? ORDER BY mp.created_at DESC", 
                  (user_id,))
        plans = c.fetchall()
        conn.close()
        return plans
        
    def get_marketing_plan(self, plan_id):
        """获取单个营销方案"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT plan_name, plan_data, created_at FROM marketing_plans WHERE id = ?", 
                  (plan_id,))
        plan = c.fetchone()
        conn.close()
        return plan    
        
    def add_data_import(self, user_id, import_name, file_path, data_count, platform):
        """添加数据导入记录"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("""
            INSERT INTO data_imports (user_id, import_name, file_path, data_count, platform, created_at) 
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (user_id, import_name, file_path, data_count, platform))
        conn.commit()
        import_id = c.lastrowid
        conn.close()
        return import_id
        
    def get_data_imports(self, user_id):
        """获取用户的数据导入记录"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("""
            SELECT id, import_name, file_path, data_count, platform, created_at 
            FROM data_imports 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        """, (user_id,))
        imports = c.fetchall()
        conn.close()
        return imports
        
    def get_latest_marketing_plan(self, user_id):
        """获取用户最新的营销方案"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT plan_name, plan_data, created_at 
                FROM marketing_plans 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT 1
            """, (user_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"获取最新营销方案失败: {e}")
            return None
        
    def save_user_settings(self, user_id, **settings):
        """保存用户设置"""
        try:
            cursor = self.conn.cursor()
            
            # 检查是否已有设置记录
            cursor.execute("SELECT id FROM user_settings WHERE user_id = ?", (user_id,))
            existing = cursor.fetchone()
            
            if existing:
                # 更新现有设置
                set_clause = ", ".join([f"{key} = ?" for key in settings.keys()])
                values = list(settings.values()) + [user_id]
                cursor.execute(f"UPDATE user_settings SET {set_clause} WHERE user_id = ?", values)
            else:
                # 创建新设置记录
                columns = ["user_id"] + list(settings.keys())
                placeholders = ["?"] * len(columns)
                values = [user_id] + list(settings.values())
                
                cursor.execute(f"""
                    INSERT INTO user_settings ({', '.join(columns)}) 
                    VALUES ({', '.join(placeholders)})
                """, values)
            
            self.conn.commit()
            return True
            
        except Exception as e:
            print(f"保存用户设置失败: {e}")
            return False
    
    def get_user_settings(self, user_id):
        """获取用户设置"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"获取用户设置失败: {e}")
            return None    