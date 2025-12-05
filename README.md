# Community Backend API

FastAPI를 사용한 커뮤니티 백엔드 API 프로젝트

## 기술 스택

![FastAPI](https://img.shields.io/badge/FastAPI-0.120.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColo=white)

- **SQLAlchemy** 2.0.44 - ORM
- **Alembic** 1.17.2 - 데이터베이스 마이그레이션
- **Pydantic** 2.12.5 - 데이터 검증
- **Uvicorn** 0.34.0 - ASGI 서버
- **Argon2-cffi** - 비밀번호 해싱 (Argon2)

## 프로젝트 구조

```
assignment/
├── app/
│   ├── controllers/          # 비즈니스 로직 (OOP)
│   │   ├── auth_controller.py
│   │   ├── user_controller.py
│   │   ├── post_controller.py
│   │   └── comment_controller.py
│   ├── models/               # 데이터베이스 모델
│   │   ├── user_model.py
│   │   ├── post_model.py
│   │   └── comment_model.py
│   ├── routers/              # API 엔드포인트
│   │   ├── auth_router.py
│   │   ├── user_router.py
│   │   ├── post_router.py
│   │   └── comment_router.py
│   ├── schemas/              # Pydantic 스키마
│   │   ├── auth_schema.py
│   │   ├── user_schema.py
│   │   ├── post_schema.py
│   │   └── comment_schema.py
│   ├── utils/                # 유틸리티
│   │   ├── security.py       # 비밀번호 해싱/검증
│   │   └── db_utils.py       # DB 트랜잭션 헬퍼
│   ├── database.py           # 데이터베이스 연결
│   └── exceptions.py         # 커스텀 예외 클래스
├── alembic/                  # 마이그레이션 파일
├── main.py                   # 애플리케이션 진입점
├── requirements.txt
└── README.md
```

## 주요 기능

### 인증 (Auth)
- 로그인 (이메일, 비밀번호)
- 로그아웃

### 사용자 (Users)
- 회원가입 (이메일, 닉네임, 비밀번호, 비밀번호 확인)
- 회원 조회 (목록, 상세)
- 회원정보 수정 (닉네임)
- 회원 탈퇴
- 비밀번호 검증: 대문자, 소문자, 숫자, 특수문자 각 1개 이상 필수
- 비밀번호 해싱: Argon2 알고리즘 사용

### 게시글 (Posts)
- 게시글 작성 (제목, 내용, 이미지 경로, **Header X-User-ID 필수**)
- 게시글 조회
  - 목록: 댓글 개수 포함, **최신순 정렬**
  - 상세: 댓글 목록 포함, 조회수 자동 증가
- 게시글 수정 (작성자만 가능, **Header X-User-ID 필수**)
- 게시글 삭제 (작성자만 가능, **Header X-User-ID 필수**)
- **RESTful 댓글 엔드포인트**: `/posts/{id}/comments`

### 댓글 (Comments)
- 게시글의 댓글 목록 조회 (`GET /posts/{post_id}/comments`, **작성순 정렬**)
- 게시글에 댓글 작성 (`POST /posts/{post_id}/comments`, **Header X-User-ID 필수**)
- 특정 댓글 조회 (`GET /comments/{comment_id}`)
- 댓글 수정 (작성자만 가능, **Header X-User-ID 필수**)
- 댓글 삭제 (작성자만 가능, **Header X-User-ID 필수**)


## 설치 및 실행

### 1. 가상환경 생성 및 활성화

#### 방법 1: venv 사용

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

#### 방법 2: conda 사용

```bash
# 새로운 가상환경 생성 (Python 3.13 사용)
conda create -n community-backend python=3.13

# 가상환경 활성화
conda activate community-backend

# 가상환경 비활성화 (필요시)
conda deactivate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 데이터베이스 마이그레이션

```bash
alembic upgrade head
```

### 4. 서버 실행

```bash
uvicorn main:app --reload
```

서버 실행 후 다음 URL에서 확인 가능:
- API 문서: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 엔드포인트

### Auth
- `POST /auth/login` - 로그인
- `POST /auth/logout` - 로그아웃

### Users
- `POST /api/users/` - 회원가입
- `GET /api/users/` - 전체 회원 조회
- `GET /api/users/{user_id}` - 회원 상세 조회
- `PUT /api/users/{user_id}` - 회원정보 수정 (본인만 가능)
- `DELETE /api/users/{user_id}` - 회원 탈퇴 (본인만 가능, **Header: X-User-ID**)

### Posts
- `POST /posts/` - 게시글 작성 (**Header: X-User-ID**)
- `GET /posts/` - 게시글 목록 조회 (댓글 개수 포함)
- `GET /posts/{post_id}` - 게시글 상세 조회 (댓글 목록 포함, 조회수 증가)
- `PUT /posts/{post_id}` - 게시글 수정 (작성자만 가능, **Header: X-User-ID**)
- `DELETE /posts/{post_id}` - 게시글 삭제 (작성자만 가능, **Header: X-User-ID**)
- `GET /posts/{post_id}/comments` - 게시글의 댓글 목록 조회
- `POST /posts/{post_id}/comments` - 게시글에 댓글 작성 (**Header: X-User-ID**)

### Comments
- `GET /comments/{comment_id}` - 특정 댓글 조회
- `PUT /comments/{comment_id}` - 댓글 수정 (작성자만 가능, **Header: X-User-ID**)
- `DELETE /comments/{comment_id}` - 댓글 삭제 (작성자만 가능, **Header: X-User-ID**)

## 데이터베이스 스키마

### Users
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | Integer | Primary Key |
| email | String | 이메일 (고유) |
| nickname | String | 닉네임 |
| hashed_password | String | 비밀번호 (Argon2 해시) |

### Posts
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | Integer | Primary Key |
| title | String(100) | 제목 |
| content | Text | 내용 |
| image_url | String(500) | 이미지 파일 경로 (선택) |
| created_at | DateTime | 작성일시 |
| view_count | Integer | 조회수 |
| like_count | Integer | 좋아요 수 |
| author_id | Integer | 작성자 ID (FK → Users) |

### Comments
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | Integer | Primary Key |
| content | Text | 댓글 내용 |
| created_at | DateTime | 작성일시 |
| post_id | Integer | 게시글 ID (FK → Posts) |
| author_id | Integer | 작성자 ID (FK → Users) |

## 외래키 관계 (CASCADE DELETE)

- **User 삭제** → 관련 Post 자동 삭제 → 관련 Comment 자동 삭제
- **Post 삭제** → 관련 Comment 자동 삭제

## 예외 처리
### 커스텀 예외 클래스 (app/exceptions.py)

| 예외 클래스 | 상태 코드 | 설명 |
|------------|----------|------|
| `NotFoundException` | 404 | 리소스를 찾을 수 없을 때 |
| `AlreadyExistsException` | 409 | 리소스가 이미 존재할 때 (이메일/닉네임 중복) |
| `UnauthorizedException` | 401 | 인증 실패 (로그인 실패) |
| `ForbiddenException` | 403 | 권한 없음 (작성자 불일치) |
| `InvalidDataException` | 400 | 유효하지 않은 데이터 |
| `DatabaseException` | 500 | 데이터베이스 오류 |

### HTTP 상태 코드

| 상태 코드 | 설명 | 예시 |
|----------|------|------|
| 200 OK | 조회/수정 성공 | GET, PUT 성공 |
| 201 Created | 생성 성공 | POST 성공 (회원가입, 게시글 작성 등) |
| 204 No Content | 삭제 성공 | DELETE 성공 |
| 400 Bad Request | 잘못된 요청 | InvalidDataException |
| 401 Unauthorized | 인증 실패 | UnauthorizedException |
| 403 Forbidden | 권한 없음 | ForbiddenException |
| 404 Not Found | 리소스 없음 | NotFoundException |
| 409 Conflict | 리소스 충돌 | AlreadyExistsException |
| 422 Unprocessable Entity | 검증 실패 | 비밀번호 규칙 위반, 필수 필드 누락 |
| 500 Internal Server Error | 서버 오류 | DatabaseException, SQLAlchemyError |

### 에러 응답 형식

```json
{
  "error": "NotFoundException",
  "message": "리소스를 찾을 수 없습니다",
  "path": "/api/users/999"
}
```

## 데이터 검증

### 회원가입
- **이메일**: 유효한 이메일 형식
- **닉네임**: 1~10자
- **비밀번호**: 8~20자, 대문자/소문자/숫자/특수문자 각 1개 이상 필수
- **비밀번호 확인**: 비밀번호와 일치 여부 검증

### 로그인
- **이메일**: 유효한 이메일 형식
- **비밀번호**: Argon2를 통한 해시 비교

### 게시글
- **제목**: 1~100자
- **내용**: 필수
- **이미지 경로**: 선택 (최대 500자)

### 댓글
- **내용**: 필수

## 아키텍처

### 계층 구조
- **Router → Controller → Model**: 명확한 역할 분리
- **OOP 기반 Controller**: 모든 컨트롤러를 클래스로 구현
- **의존성 주입**: FastAPI Depends를 통한 DB 세션 관리
- **RESTful API**: 리소스 간 계층적 관계를 URL로 표현 (`/posts/{id}/comments`)

### 예외 처리 전략
- **전역 예외 핸들러**: main.py에서 모든 커스텀 예외를 중앙 집중식으로 처리
- **계층별 예외 변환**: SQLAlchemy 예외를 애플리케이션 예외로 변환
- **일관된 에러 응답**: 모든 에러는 동일한 JSON 형식으로 반환

### 데이터베이스 트랜잭션 관리
- **Context Manager 패턴**: `db_transaction()` 사용으로 안전한 트랜잭션 처리
- **자동 롤백**: 예외 발생 시 자동으로 롤백
- **에러 변환**: `IntegrityError`는 `InvalidDataException`으로, 기타 DB 에러는 `DatabaseException`으로 변환
```python
# 사용 예시
with db_transaction(self.db):
    self.db.add(new_user)
# 자동 commit 또는 예외 발생 시 자동 rollback
```

## 개발 환경

- Python 3.13+
- SQLite 3
