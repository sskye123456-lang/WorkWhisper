# Database Service
import sqlite3
import json
from datetime import datetime
from typing import Optional
from pathlib import Path

from app.models.user import User, UserState, PersonaType
from app.config import config


class Database:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or config.DATABASE_PATH
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                open_id TEXT PRIMARY KEY,
                state TEXT DEFAULT 'new',
                current_persona TEXT,
                quiz_progress INTEGER DEFAULT 0,
                quiz_answers TEXT DEFAULT '[]',
                reinforcement_count INTEGER DEFAULT 0,
                reinforcement_reset_date TEXT DEFAULT '',
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.commit()
        conn.close()

    def get_user(self, open_id: str) -> Optional[User]:
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE open_id = ?", (open_id,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        return User(
            open_id=row["open_id"],
            state=UserState(row["state"]),
            current_persona=PersonaType(row["current_persona"]) if row["current_persona"] else None,
            quiz_progress=row["quiz_progress"],
            quiz_answers=json.loads(row["quiz_answers"]),
            reinforcement_count=row["reinforcement_count"],
            reinforcement_reset_date=row["reinforcement_reset_date"],
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else datetime.now(),
            updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else datetime.now(),
        )

    def create_user(self, open_id: str) -> User:
        now = datetime.now()
        user = User(open_id=open_id, state=UserState.NEW, created_at=now, updated_at=now)
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO users 
            (open_id, state, current_persona, quiz_progress, quiz_answers, 
             reinforcement_count, reinforcement_reset_date, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user.open_id, user.state.value,
            user.current_persona.value if user.current_persona else None,
            user.quiz_progress, json.dumps(user.quiz_answers),
            user.reinforcement_count, user.reinforcement_reset_date,
            user.created_at.isoformat(), user.updated_at.isoformat(),
        ))
        conn.commit()
        conn.close()
        return user

    def update_user(self, user: User) -> User:
        user.updated_at = datetime.now()
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET
                state = ?, current_persona = ?, quiz_progress = ?,
                quiz_answers = ?, reinforcement_count = ?,
                reinforcement_reset_date = ?, updated_at = ?
            WHERE open_id = ?
        """, (
            user.state.value,
            user.current_persona.value if user.current_persona else None,
            user.quiz_progress, json.dumps(user.quiz_answers),
            user.reinforcement_count, user.reinforcement_reset_date,
            user.updated_at.isoformat(), user.open_id,
        ))
        conn.commit()
        conn.close()
        return user

    def save_quiz_answer(self, open_id: str, question_id: int, answer: str) -> User:
        user = self.get_user(open_id)
        if not user:
            user = self.create_user(open_id)
        while len(user.quiz_answers) < question_id - 1:
            user.quiz_answers.append("")
        if question_id <= len(user.quiz_answers):
            user.quiz_answers[question_id - 1] = answer
        else:
            user.quiz_answers.append(answer)
        user.quiz_progress = question_id
        return self.update_user(user)

    def set_persona(self, open_id: str, persona: PersonaType) -> User:
        user = self.get_user(open_id)
        if not user:
            user = self.create_user(open_id)
        user.current_persona = persona
        user.state = UserState.HAS_PERSONA
        return self.update_user(user)

    def use_reinforcement(self, open_id: str):
        user = self.get_user(open_id)
        if not user:
            user = self.create_user(open_id)
        today = datetime.now().strftime("%Y-%m-%d")
        if user.reinforcement_reset_date != today:
            user.reinforcement_count = 0
            user.reinforcement_reset_date = today
        if user.reinforcement_count >= config.REINFORCEMENT_DAILY_LIMIT:
            return user, False
        user.reinforcement_count += 1
        return self.update_user(user), True


db = Database()
