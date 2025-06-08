from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import databases
import sqlalchemy
from datetime import date, time
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database setup
DATABASE_URL = "sqlite:///./blackrooms.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Define all tables
position = sqlalchemy.Table(
    "position",
    metadata,
    sqlalchemy.Column("position_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(255)),
    sqlalchemy.Column("access_level", sqlalchemy.Integer),
)

employee = sqlalchemy.Table(
    "employee",
    metadata,
    sqlalchemy.Column("employee_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("full_name", sqlalchemy.Text),
    sqlalchemy.Column("position_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("position.position_id")),
    sqlalchemy.Column("login", sqlalchemy.String(255)),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
)

client = sqlalchemy.Table(
    "client",
    metadata,
    sqlalchemy.Column("client_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("full_name", sqlalchemy.Text),
    sqlalchemy.Column("phone", sqlalchemy.String(255)),
    sqlalchemy.Column("email", sqlalchemy.String(255)),
    sqlalchemy.Column("birth_date", sqlalchemy.Date),
    sqlalchemy.Column("login", sqlalchemy.String(255), unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
)

quest = sqlalchemy.Table(
    "quest",
    metadata,
    sqlalchemy.Column("quest_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(255)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("difficulty", sqlalchemy.Integer),
    sqlalchemy.Column("duration", sqlalchemy.Integer),
    sqlalchemy.Column("price", sqlalchemy.Integer),
)

room = sqlalchemy.Table(
    "room",
    metadata,
    sqlalchemy.Column("room_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(255)),
    sqlalchemy.Column("type", sqlalchemy.String(255)),
    sqlalchemy.Column("capacity", sqlalchemy.Integer),
    sqlalchemy.Column("is_available", sqlalchemy.Boolean),
)

schedule = sqlalchemy.Table(
    "schedule",
    metadata,
    sqlalchemy.Column("schedule_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("quest_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("quest.quest_id")),
    sqlalchemy.Column("room_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("room.room_id")),
    sqlalchemy.Column("date", sqlalchemy.Date),
    sqlalchemy.Column("start_time", sqlalchemy.Time),
    sqlalchemy.Column("end_time", sqlalchemy.Time),
)

booking = sqlalchemy.Table(
    "booking",
    metadata,
    sqlalchemy.Column("booking_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("client_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("client.client_id")),
    sqlalchemy.Column("schedule_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("schedule.schedule_id")),
    sqlalchemy.Column("employee_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("employee.employee_id")),
    sqlalchemy.Column("status", sqlalchemy.String(255)),
    sqlalchemy.Column("participants_count", sqlalchemy.Integer),
)

payment = sqlalchemy.Table(
    "payment",
    metadata,
    sqlalchemy.Column("payment_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("booking_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("booking.booking_id")),
    sqlalchemy.Column("payment_method", sqlalchemy.String(255)),
    sqlalchemy.Column("amount", sqlalchemy.Integer),
    sqlalchemy.Column("payment_date", sqlalchemy.Date),
)

review = sqlalchemy.Table(
    "review",
    metadata,
    sqlalchemy.Column("review_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("client_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("client.client_id")),
    sqlalchemy.Column("quest_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("quest.quest_id")),
    sqlalchemy.Column("text", sqlalchemy.Text),
    sqlalchemy.Column("rating", sqlalchemy.Integer),
)

service = sqlalchemy.Table(
    "service",
    metadata,
    sqlalchemy.Column("service_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(255)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("price", sqlalchemy.Integer),
    sqlalchemy.Column("booking_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("booking.booking_id")),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()
    await insert_initial_data()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

async def insert_initial_data():
    # Проверяем, есть ли уже данные в таблицах
    positions = await database.fetch_all(position.select())
    if not positions:
        # Добавляем начальные данные
        await database.execute_many(
            position.insert(),
            [
                {"position_id": 1, "title": "Администратор", "access_level": 3},
                {"position_id": 2, "title": "Игровой мастер", "access_level": 2},
                {"position_id": 3, "title": "Уборщик", "access_level": 1},
            ]
        )

        # Хешируем пароли сотрудников перед сохранением
        await database.execute_many(
            employee.insert(),
            [
                {"employee_id": 1, "full_name": "Иванов Иван Иванович", "position_id": 1,
                 "login": "admin", "password": pwd_context.hash("admin123")},
                {"employee_id": 2, "full_name": "Петров Петр Петрович", "position_id": 2,
                 "login": "master1", "password": pwd_context.hash("master123")},
                {"employee_id": 3, "full_name": "Сидорова Анна Михайловна", "position_id": 2,
                 "login": "master2", "password": pwd_context.hash("master456")},
            ]
        )

        # Хешируем пароли клиентов перед сохранением
        await database.execute_many(
            client.insert(),
            [
                {"client_id": 1, "full_name": "Смирнов Алексей Владимирович", "phone": "+79161234567",
                 "email": "smirnov@mail.ru", "birth_date": date(1990, 5, 15),
                 "login": "smirnov", "password": pwd_context.hash("client123")},
                {"client_id": 2, "full_name": "Кузнецова Елена Сергеевна", "phone": "+79269876543",
                 "email": "kuznetsova@gmail.com", "birth_date": date(1985, 8, 22),
                 "login": "kuznetsova", "password": pwd_context.hash("client456")},
                {"client_id": 3, "full_name": "Попов Дмитрий Александрович", "phone": "+79031112233",
                 "email": "popov@yandex.ru", "birth_date": date(1995, 3, 10),
                 "login": "popov", "password": pwd_context.hash("client789")},
            ]
        )

        await database.execute_many(
            quest.insert(),
            [
                {"quest_id": 1, "title": "Проклятый замок", "description": "Найдите выход из проклятого замка", "difficulty": 4, "duration": 60, "price": 2500},
                {"quest_id": 2, "title": "Лаборатория безумного ученого", "description": "Остановите безумного ученого", "difficulty": 5, "duration": 75, "price": 3000},
                {"quest_id": 3, "title": "Побег из тюрьмы", "description": "Спланируйте и осуществите побег", "difficulty": 3, "duration": 45, "price": 2000},
            ]
        )

        await database.execute_many(
            room.insert(),
            [
                {"room_id": 1, "title": "Комната 1", "type": "Стандарт", "capacity": 5, "is_available": True},
                {"room_id": 2, "title": "Комната 2", "type": "Премиум", "capacity": 6, "is_available": True},
                {"room_id": 3, "title": "Комната 3", "type": "Стандарт", "capacity": 4, "is_available": False},
            ]
        )

        await database.execute_many(
            schedule.insert(),
            [
                {"schedule_id": 1, "quest_id": 1, "room_id": 1, "date": date(2023, 12, 15), "start_time": time(18, 0), "end_time": time(19, 0)},
                {"schedule_id": 2, "quest_id": 2, "room_id": 2, "date": date(2023, 12, 15), "start_time": time(19, 30), "end_time": time(20, 45)},
                {"schedule_id": 3, "quest_id": 3, "room_id": 1, "date": date(2023, 12, 16), "start_time": time(17, 0), "end_time": time(17, 45)},
            ]
        )

        await database.execute_many(
            booking.insert(),
            [
                {"booking_id": 1, "client_id": 1, "schedule_id": 1, "employee_id": 2, "status": "Подтверждено", "participants_count": 4},
                {"booking_id": 2, "client_id": 2, "schedule_id": 2, "employee_id": 3, "status": "Оплачено", "participants_count": 5},
                {"booking_id": 3, "client_id": 3, "schedule_id": 3, "employee_id": 2, "status": "Забронировано", "participants_count": 3},
            ]
        )

        await database.execute_many(
            payment.insert(),
            [
                {"payment_id": 1, "booking_id": 1, "payment_method": "Карта", "amount": 2500, "payment_date": date(2023, 12, 10)},
                {"payment_id": 2, "booking_id": 2, "payment_method": "Наличные", "amount": 3000, "payment_date": date(2023, 12, 12)},
                {"payment_id": 3, "booking_id": 3, "payment_method": "Карта", "amount": 2000, "payment_date": date(2023, 12, 14)},
            ]
        )

        await database.execute_many(
            review.insert(),
            [
                {"review_id": 1, "client_id": 1, "quest_id": 1, "text": "Отличный квест, очень атмосферно!", "rating": 5},
                {"review_id": 2, "client_id": 2, "quest_id": 2, "text": "Сложновато, но интересно", "rating": 4},
                {"review_id": 3, "client_id": 3, "quest_id": 3, "text": "Хороший квест для новичков", "rating": 4},
            ]
        )

        await database.execute_many(
            service.insert(),
            [
                {"service_id": 1, "title": "Фотосессия", "description": "Профессиональные фото с квеста", "price": 500, "booking_id": 1},
                {"service_id": 2, "title": "Видеосъемка", "description": "Запись прохождения квеста", "price": 800, "booking_id": 2},
                {"service_id": 3, "title": "Дополнительный актер", "description": "Актер для усиления погружения", "price": 1000, "booking_id": 3},
            ]
        )

# Pydantic models
class PositionBase(BaseModel):
    title: str
    access_level: int

class PositionCreate(PositionBase):
    pass

class Position(PositionBase):
    position_id: int

    class Config:
        from_attributes = True

class EmployeeBase(BaseModel):
    full_name: str
    position_id: int
    login: str

class EmployeeCreate(EmployeeBase):
    password: str

class Employee(EmployeeBase):
    employee_id: int

    class Config:
        from_attributes = True

class ClientBase(BaseModel):
    full_name: str
    phone: str
    email: str
    birth_date: date
    login: str

class ClientCreate(ClientBase):
    password: str

class Client(ClientBase):
    client_id: int

    class Config:
        from_attributes = True

class ClientLogin(BaseModel):
    login: str
    password: str

class QuestBase(BaseModel):
    title: str
    description: str
    difficulty: int
    duration: int
    price: int

class QuestCreate(QuestBase):
    pass

class Quest(QuestBase):
    quest_id: int

    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    title: str
    type: str
    capacity: int
    is_available: bool

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    room_id: int

    class Config:
        from_attributes = True

class ScheduleBase(BaseModel):
    quest_id: int
    room_id: int
    date: date
    start_time: time
    end_time: time

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    schedule_id: int

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    client_id: int
    schedule_id: int
    employee_id: int
    status: str
    participants_count: int

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    booking_id: int

    class Config:
        from_attributes = True

class PaymentBase(BaseModel):
    booking_id: int
    payment_method: str
    amount: int
    payment_date: date

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    payment_id: int

    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    client_id: int
    quest_id: int
    text: str
    rating: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    review_id: int

    class Config:
        from_attributes = True

class ServiceBase(BaseModel):
    title: str
    description: str
    price: int
    booking_id: int

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    service_id: int

    class Config:
        from_attributes = True

# Position routes
@app.post("/positions/", response_model=Position)
async def create_position(position: PositionCreate):
    query = position.insert().values(
        title=position.title,
        access_level=position.access_level
    )
    last_record_id = await database.execute(query)
    return {**position.dict(), "position_id": last_record_id}

@app.get("/positions/", response_model=List[Position])
async def read_positions():
    query = position.select()
    return await database.fetch_all(query)

@app.get("/positions/{position_id}", response_model=Position)
async def read_position(position_id: int):
    query = position.select().where(position.c.position_id == position_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Position not found")
    return result

@app.put("/positions/{position_id}", response_model=Position)
async def update_position(position_id: int, position_data: PositionCreate):
    query = (
        position.update()
        .where(position.c.position_id == position_id)
        .values(**position_data.dict())
    )
    await database.execute(query)
    return {**position_data.dict(), "position_id": position_id}

@app.delete("/positions/{position_id}")
async def delete_position(position_id: int):
    query = position.delete().where(position.c.position_id == position_id)
    await database.execute(query)
    return {"message": "Position deleted successfully"}

# Employee routes
@app.post("/employees/", response_model=Employee)
async def create_employee(employee_data: EmployeeCreate):
    # 1. Хешируем пароль перед сохранением
    hashed_password = pwd_context.hash(employee_data.password)

    # 2. Используем SQLAlchemy-таблицу employee для вставки
    query = employee.insert().values(
        full_name=employee_data.full_name,
        position_id=employee_data.position_id,
        login=employee_data.login,
        password=hashed_password  # Сохраняем хеш вместо plaintext
    )

    # 3. Выполняем запрос и получаем ID новой записи
    employee_id = await database.execute(query)

    # 4. Получаем созданного сотрудника (без пароля в ответе)
    created_employee = await database.fetch_one(
        employee.select().where(employee.c.employee_id == employee_id)
    )

    if not created_employee:
        raise HTTPException(status_code=500, detail="Failed to create employee")

    # 5. Возвращаем данные, исключая пароль
    return {**dict(created_employee), "password": None}

@app.get("/employees/", response_model=List[Employee])
async def read_employees():
    query = employee.select()
    return await database.fetch_all(query)

@app.get("/employees/{employee_id}", response_model=Employee)
async def read_employee(employee_id: int):
    query = employee.select().where(employee.c.employee_id == employee_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Employee not found")
    return result

@app.put("/employees/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, employee_data: EmployeeCreate):
    # Получаем текущие данные сотрудника
    current_employee = await database.fetch_one(
        employee.select().where(employee.c.employee_id == employee_id)
    )
    if not current_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Подготавливаем данные для обновления
    update_data = employee_data.dict(exclude_unset=True)

    # Если передан пароль — хешируем его
    if "password" in update_data:
        update_data["password"] = pwd_context.hash(update_data["password"])

    # Обновляем запись
    query = (
        employee.update()
        .where(employee.c.employee_id == employee_id)
        .values(**update_data)
    )
    await database.execute(query)

    # Возвращаем обновленные данные (без пароля)
    updated_employee = await database.fetch_one(
        employee.select().where(employee.c.employee_id == employee_id)
    )
    return {**dict(updated_employee), "password": None}  # Явно убираем пароль

@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: int):
    query = employee.delete().where(employee.c.employee_id == employee_id)
    await database.execute(query)
    return {"message": "Employee deleted successfully"}

# Client routes
@app.post("/clients/register/", response_model=Client)
async def register_client(client_data: ClientCreate):
    # Проверяем, нет ли уже клиента с таким логином
    existing_client = await database.fetch_one(
        client.select().where(client.c.login == client_data.login)
    )
    if existing_client:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким логином уже существует"
        )

    # Хешируем пароль перед сохранением
    hashed_password = pwd_context.hash(client_data.password)

    # Создаем нового клиента
    query = client.insert().values(
        full_name=client_data.full_name,
        phone=client_data.phone,
        email=client_data.email,
        birth_date=client_data.birth_date,
        login=client_data.login,
        password=hashed_password
    )
    client_id = await database.execute(query)

    # Получаем созданного клиента без пароля
    new_client = await database.fetch_one(
        client.select().where(client.c.client_id == client_id)
    )

    return {**dict(new_client), "password": "*****"}


@app.post("/clients/login/")
async def login_client(credentials: ClientLogin):
    query = client.select().where(client.c.login == credentials.login)
    client_data = await database.fetch_one(query)

    if not client_data or not pwd_context.verify(credentials.password, client_data["password"]):
        raise HTTPException(
            status_code=401,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"message": "Успешный вход", "client_id": client_data["client_id"]}


@app.post("/clients/change-password/")
async def change_client_password(client_id: int, old_password: str, new_password: str):
    query = client.select().where(client.c.client_id == client_id)
    client_data = await database.fetch_one(query)

    if not client_data or not pwd_context.verify(old_password, client_data["password"]):
        raise HTTPException(
            status_code=401,
            detail="Неверный текущий пароль",
        )

    hashed_new_password = pwd_context.hash(new_password)
    update_query = (
        client.update()
        .where(client.c.client_id == client_id)
        .values(password=hashed_new_password)
    )
    await database.execute(update_query)

    return {"message": "Пароль успешно изменен"}

@app.get("/clients/", response_model=List[Client])
async def read_clients():
    query = client.select()
    return await database.fetch_all(query)

@app.get("/clients/{client_id}", response_model=Client)
async def read_client(client_id: int):
    query = client.select().where(client.c.client_id == client_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Client not found")
    return result

@app.put("/clients/{client_id}", response_model=Client)
async def update_client(client_id: int, client_data: ClientCreate):
    # Получаем текущие данные клиента
    current_client = await database.fetch_one(
        client.select().where(client.c.client_id == client_id)
    )
    if not current_client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Подготавливаем данные для обновления
    update_data = client_data.dict(exclude_unset=True)

    # Если передан пароль — хешируем его
    if "password" in update_data:
        update_data["password"] = pwd_context.hash(update_data["password"])

    # Обновляем запись
    query = (
        client.update()
        .where(client.c.client_id == client_id)
        .values(**update_data)
    )
    await database.execute(query)

    # Возвращаем обновленные данные (без пароля)
    updated_client = await database.fetch_one(
        client.select().where(client.c.client_id == client_id)
    )
    return {**dict(updated_client), "password": None}

@app.delete("/clients/{client_id}")
async def delete_client(client_id: int):
    query = client.delete().where(client.c.client_id == client_id)
    await database.execute(query)
    return {"message": "Client deleted successfully"}

# Quest routes
@app.post("/quests/", response_model=Quest)
async def create_quest(quest_data: QuestCreate):
    query = quest.insert().values(
        title=quest_data.title,
        description=quest_data.description,
        difficulty=quest_data.difficulty,
        duration=quest_data.duration,
        price=quest_data.price
    )

    quest_id = await database.execute(query)
    created_quest = await database.fetch_one(
        quest.select().where(quest.c.quest_id == quest_id)
    )

    if not created_quest:
        raise HTTPException(status_code=500, detail="Failed to create quest")
    return created_quest

@app.get("/quests/", response_model=List[Quest])
async def read_quests():
    query = quest.select()
    return await database.fetch_all(query)

@app.get("/quests/{quest_id}", response_model=Quest)
async def read_quest(quest_id: int):
    query = quest.select().where(quest.c.quest_id == quest_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Quest not found")
    return result

@app.put("/quests/{quest_id}", response_model=Quest)
async def update_quest(quest_id: int, quest_data: QuestCreate):
    query = (
        quest.update()
        .where(quest.c.quest_id == quest_id)
        .values(**quest_data.dict())
    )
    await database.execute(query)
    return {**quest_data.dict(), "quest_id": quest_id}

@app.delete("/quests/{quest_id}")
async def delete_quest(quest_id: int):
    query = quest.delete().where(quest.c.quest_id == quest_id)
    await database.execute(query)
    return {"message": "Quest deleted successfully"}

# Room routes
@app.post("/rooms/", response_model=Room)
async def create_room(room: RoomCreate):
    query = room.insert().values(**room.dict())
    last_record_id = await database.execute(query)
    return {**room.dict(), "room_id": last_record_id}

@app.get("/rooms/", response_model=List[Room])
async def read_rooms():
    query = room.select()
    return await database.fetch_all(query)

@app.get("/rooms/{room_id}", response_model=Room)
async def read_room(room_id: int):
    query = room.select().where(room.c.room_id == room_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Room not found")
    return result

@app.put("/rooms/{room_id}", response_model=Room)
async def update_room(room_id: int, room_data: RoomCreate):
    query = (
        room.update()
        .where(room.c.room_id == room_id)
        .values(**room_data.dict())
    )
    await database.execute(query)
    return {**room_data.dict(), "room_id": room_id}

@app.delete("/rooms/{room_id}")
async def delete_room(room_id: int):
    query = room.delete().where(room.c.room_id == room_id)
    await database.execute(query)
    return {"message": "Room deleted successfully"}

# Schedule routes
@app.post("/schedules/", response_model=Schedule)
async def create_schedule(schedule_data: ScheduleCreate):
    query = schedule.insert().values(**schedule_data.dict())
    schedule_id = await database.execute(query)
    return await database.fetch_one(schedule.select().where(schedule.c.schedule_id == schedule_id))

@app.get("/schedules/", response_model=List[Schedule])
async def read_schedules():
    query = schedule.select()
    return await database.fetch_all(query)

@app.get("/schedules/{schedule_id}", response_model=Schedule)
async def read_schedule(schedule_id: int):
    query = schedule.select().where(schedule.c.schedule_id == schedule_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return result

@app.put("/schedules/{schedule_id}", response_model=Schedule)
async def update_schedule(schedule_id: int, schedule_data: ScheduleCreate):
    await database.execute(
        schedule.update()
        .where(schedule.c.schedule_id == schedule_id)
        .values(**schedule_data.dict())
    )
    return await database.fetch_one(schedule.select().where(schedule.c.schedule_id == schedule_id))


@app.delete("/schedules/{schedule_id}")
async def delete_schedule(schedule_id: int):
    await database.execute(schedule.delete().where(schedule.c.schedule_id == schedule_id))
    return {"message": "Schedule deleted"}

# Booking routes
@app.post("/bookings/", response_model=Booking)
async def create_booking(booking_data: BookingCreate):
    # Вставляем данные в таблицу booking
    query = booking.insert().values(**booking_data.dict())
    booking_id = await database.execute(query)

    # Получаем созданную запись
    created_booking = await database.fetch_one(
        booking.select().where(booking.c.booking_id == booking_id)
    )

    if not created_booking:
        raise HTTPException(status_code=500, detail="Failed to create booking")

    return created_booking

@app.get("/bookings/", response_model=List[Booking])
async def read_bookings():
    query = booking.select()
    return await database.fetch_all(query)

@app.get("/bookings/{booking_id}", response_model=Booking)
async def read_booking(booking_id: int):
    query = booking.select().where(booking.c.booking_id == booking_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Booking not found")
    return result

@app.put("/bookings/{booking_id}", response_model=Booking)
async def update_booking(booking_id: int, booking_data: BookingCreate):
    query = (
        booking.update()
        .where(booking.c.booking_id == booking_id)
        .values(**booking_data.dict())
    )
    await database.execute(query)
    return {**booking_data.dict(), "booking_id": booking_id}

@app.delete("/bookings/{booking_id}")
async def delete_booking(booking_id: int):
    query = booking.delete().where(booking.c.booking_id == booking_id)
    await database.execute(query)
    return {"message": "Booking deleted successfully"}

# Payment routes
@app.post("/payments/", response_model=Payment)
async def create_payment(payment: PaymentCreate):
    query = payment.insert().values(**payment.dict())
    last_record_id = await database.execute(query)
    return {**payment.dict(), "payment_id": last_record_id}

@app.get("/payments/", response_model=List[Payment])
async def read_payments():
    query = payment.select()
    return await database.fetch_all(query)

@app.get("/payments/{payment_id}", response_model=Payment)
async def read_payment(payment_id: int):
    query = payment.select().where(payment.c.payment_id == payment_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Payment not found")
    return result

@app.put("/payments/{payment_id}", response_model=Payment)
async def update_payment(payment_id: int, payment_data: PaymentCreate):
    query = (
        payment.update()
        .where(payment.c.payment_id == payment_id)
        .values(**payment_data.dict())
    )
    await database.execute(query)
    return {**payment_data.dict(), "payment_id": payment_id}

@app.delete("/payments/{payment_id}")
async def delete_payment(payment_id: int):
    query = payment.delete().where(payment.c.payment_id == payment_id)
    await database.execute(query)
    return {"message": "Payment deleted successfully"}

# Review routes
@app.post("/reviews/", response_model=Review)
async def create_review(review: ReviewCreate):
    query = review.insert().values(**review.dict())
    last_record_id = await database.execute(query)
    return {**review.dict(), "review_id": last_record_id}

@app.get("/reviews/", response_model=List[Review])
async def read_reviews():
    query = review.select()
    return await database.fetch_all(query)

@app.get("/reviews/{review_id}", response_model=Review)
async def read_review(review_id: int):
    query = review.select().where(review.c.review_id == review_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Review not found")
    return result

@app.put("/reviews/{review_id}", response_model=Review)
async def update_review(review_id: int, review_data: ReviewCreate):
    query = (
        review.update()
        .where(review.c.review_id == review_id)
        .values(**review_data.dict())
    )
    await database.execute(query)
    return {**review_data.dict(), "review_id": review_id}

@app.delete("/reviews/{review_id}")
async def delete_review(review_id: int):
    query = review.delete().where(review.c.review_id == review_id)
    await database.execute(query)
    return {"message": "Review deleted successfully"}

# Service routes
@app.post("/services/", response_model=Service)
async def create_service(service_data: ServiceCreate):
    query = service.insert().values(**service_data.dict())
    last_record_id = await database.execute(query)

    created_service = await database.fetch_one(
        service.select().where(service.c.service_id == last_record_id)
    )

    if not created_service:
        raise HTTPException(status_code=500, detail="Failed to create service")
    return created_service


@app.get("/services/", response_model=List[Service])
async def read_services():
    query = service.select()
    return await database.fetch_all(query)

@app.get("/services/{service_id}", response_model=Service)
async def read_service(service_id: int):
    query = service.select().where(service.c.service_id == service_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Service not found")
    return result

@app.put("/services/{service_id}", response_model=Service)
async def update_service(service_id: int, service_data: ServiceCreate):
    query = (
        service.update()
        .where(service.c.service_id == service_id)
        .values(**service_data.dict())
    )
    await database.execute(query)
    return {**service_data.dict(), "service_id": service_id}

@app.delete("/services/{service_id}")
async def delete_service(service_id: int):
    query = service.delete().where(service.c.service_id == service_id)
    await database.execute(query)
    return {"message": "Service deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)