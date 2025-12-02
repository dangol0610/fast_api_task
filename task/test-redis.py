# import redis

# r = redis.Redis(
#     host="localhost",
#     port=6379,
#     db=0,
#     decode_responses=True,
# )
# try:
#     r.ping()

#     r.set("test_key", "test_value", ex=120)
#     print("Add key with TTL 120 seconds")
#     v = r.get("test_key")
#     print(f"Value: {v}")

#     r.hset(
#         "user1",
#         mapping={
#             "name": "John",
#             "age": "30",
#             "city": "New York",
#         },
#     )
#     print("Add hashmap for user1")
#     user_data = r.hgetall("user1")
#     print(f"Userdata: {user_data}")

#     r.lpush(
#         "tasks",
#         "task1",
#         "task2",
#         "task3",
#     )
#     print("Add list of tasks")
#     tasks = r.lrange("tasks", 0, -1)
#     print(f"Tasks: {tasks}")

#     r.expire("user1", 120)
#     print("Set TTL for user1 to 120 seconds")

# except redis.ConnectionError:
#     print("Failed to connect to Redis")
# finally:
#     r.close()


def add_numbers(a: int, b: int, c: int):
    return a + b + c


print(add_numbers.__code__.co_varnames)
