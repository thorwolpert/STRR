from datetime import datetime
from datetime import timedelta
from datetime import timezone
import logging
import random
import time

import pytest
from sqlalchemy import insert
from sqlalchemy.orm import Session
from strr_api.enums.enum import ChannelType
from strr_api.models import Application
from strr_api.models import CustomerInteraction
from strr_api.models import Registration
from strr_api.models import User

logger = logging.getLogger(__name__)


@pytest.fixture
def setup_parents(session: Session, random_string, random_integer):
    """
    Creates one parent record in each table so we have valid IDs
    to link our interactions to.

    TODO: this should be part of a session wide set of fixture strategy
    """
    customer = User()
    user = User()
    session.add_all([user, customer])
    session.flush()

    reg = Registration(
        registration_type=Registration.RegistrationType.HOST,
        registration_number=random_string(10),
        sbc_account_id=random_integer(),
        status="ACTIVE",
        user_id=user.id,
        start_date=datetime.now(timezone.utc),
        expiry_date=(datetime.now(timezone.utc) + timedelta(days=365)).date(),
    )
    session.add(reg)
    session.flush()

    app = Application(
        id=random_integer(),
        application_json={},
        registration_id=reg.id,
        application_number=random_string(10),
        type="",
        registration_type=Registration.RegistrationType.HOST,
    )

    session.add(app)
    session.flush()

    return {
        "application_id": app.id,
        "customer_id": customer.id,
        "registration_id": reg.id,
        "user_id": user.id,
    }


# @pytest.fixture
# def setup_bulk_parents(request, session: Session, random_string, random_integer):
#     n_records = getattr(request, "param", 10)
#     # find the optimal chunksize for you by running test_perf
#     chunk_size = 2000 # The number of records to process per batch
#     if isinstance(n_records, dict):
#         chunk_size = n_records.get("chunk_size", 2000)
#         n_records = n_records.get("records", 10)

#     # 1. Setup Parents
#     customer = User()
#     user = User()
#     session.add_all([user, customer])
#     session.flush()

#     now = datetime.now(timezone.utc)
#     expiry = (now + timedelta(days=365)).date()

#     # Lists to hold all generated IDs across all chunks
#     all_reg_ids = []
#     all_app_ids = []

#     start_time = time.perf_counter()

#     # 2. Loop through the total records in steps of 'chunk_size'
#     for offset in range(0, n_records, chunk_size):
#         # Handle the last chunk which might be smaller than chunk_size
#         current_chunk_size = min(chunk_size, n_records - offset)

#         # A. Prepare Registration Data for THIS chunk
#         regs_data = [
#             {
#                 "registration_type": Registration.RegistrationType.HOST,
#                 # Use 'offset + i' to ensure uniqueness across all chunks
#                 "registration_number": f"REG-{offset + i}-{random_string(5)}",
#                 "sbc_account_id": random_integer() + offset + i,
#                 "status": "ACTIVE",
#                 "user_id": user.id,
#                 "start_date": now,
#                 "expiry_date": expiry,
#             }
#             for i in range(current_chunk_size)
#         ]

#         # B. Insert Registrations and extend our master list of IDs
#         chunk_reg_ids = session.scalars(
#             insert(Registration).returning(Registration.id),
#             regs_data
#         ).all()
#         all_reg_ids.extend(chunk_reg_ids)

#         # C. Prepare Application Data mapped to THIS chunk's Registration IDs
#         apps_data = [
#             {
#                 "application_json": {},
#                 "registration_id": reg_id,
#                 "application_number": f"{offset + i}".zfill(14),
#                 # "application_number": f"APP-{offset + i}-{random_string(5)}",
#                 "type": "",
#                 "registration_type": Registration.RegistrationType.HOST,
#             }
#             for i, reg_id in enumerate(chunk_reg_ids)
#         ]

#         # D. Insert Applications and extend our master list of IDs
#         chunk_app_ids = session.scalars(
#             insert(Application).returning(Application.id),
#             apps_data
#         ).all()
#         all_app_ids.extend(chunk_app_ids)

#     # 3. Flush all chunks to the database within the test transaction
#     session.flush()
#     end_time = time.perf_counter()
#     duration = end_time - start_time

#     # Print the results directly to the console
#     print(f"\n[PROFILER] Inserted {n_records} records in chunks of {chunk_size} "
#           f"-> Time: {duration:.3f} seconds")

#     return {
#         "customer_id": customer.id,
#         "user_id": user.id,
#         "record_count": n_records,
#         "registration_ids": all_reg_ids,
#         "application_ids": all_app_ids,
#     }


# @pytest.fixture
# def setup_bulk_parents(request, session: Session, random_string, random_integer):

#     # Default parameters
#     n_records = 10
#     chunk_size = 2000 # this is the optimal size discovered in test_perf
#     target_days = []     # e.g., [0, 15, 30, 45, 60]
#     target_pct = 0.0

#     # Extract test-specific parameters if they exist
#     if hasattr(request, "param") and isinstance(request.param, dict):
#         n_records = request.param.get("records", 10)
#         chunk_size = request.param.get("chunk_size", 2000)
#         target_days = request.param.get("target_days", [])
#         target_pct = request.param.get("target_pct", 0.0)

#     # 1. Setup Parents
#     customer = User()
#     user = User()
#     session.add_all([user, customer])
#     session.flush()

#     now = datetime.now(timezone.utc).date()
#     expiry_dates = []

#     # Calculate distributions IF targets were passed in
#     if target_days and target_pct > 0:
#         count_per_target = int(n_records * target_pct)
#         remaining_count = n_records - (count_per_target * len(target_days))

#         # 1. Generate targeted dates
#         for days_out in target_days:
#             target_date = now + timedelta(days=days_out)
#             expiry_dates.extend([target_date] * count_per_target)

#         # 2. Generate noise dates (distribute over 120 days, avoiding targets)
#         allowed_noise_days = [d for d in range(120) if d not in target_days]
#         for _ in range(remaining_count):
#             random_days = random.choice(allowed_noise_days)
#             expiry_dates.append(now + timedelta(days=random_days))
#     else:
#         # Fallback for standard tests: just make everything expire in 1 year
#         expiry_dates = [now + timedelta(days=365)] * n_records

#     # Shuffle the dates so they are randomized in the database
#     random.shuffle(expiry_dates)

#     # Lists to hold all generated IDs across all chunks
#     all_reg_ids = []
#     all_app_ids = []

#     start_time = time.perf_counter()

#     # 2. Loop through the total records in steps of 'chunk_size'
#     for offset in range(0, n_records, chunk_size):
#         # Handle the last chunk which might be smaller than chunk_size
#         current_chunk_size = min(chunk_size, n_records - offset)

#         # A. Prepare Registration Data for THIS chunk
#         regs_data = [
#             {
#                 "registration_type": Registration.RegistrationType.HOST,
#                 # Use 'offset + i' to ensure uniqueness across all chunks
#                 "registration_number": "H" + f"{offset + i}".zfill(13),
#                 "sbc_account_id": random_integer() + offset + i,
#                 "status": "ACTIVE",
#                 "user_id": user.id,
#                 "start_date": now,
#                 "expiry_date": expiry_dates[offset + i],
#             }
#             for i in range(current_chunk_size)
#         ]

#         # B. Insert Registrations and extend our master list of IDs
#         chunk_reg_ids = session.scalars(
#             insert(Registration).returning(Registration.id),
#             regs_data
#         ).all()
#         all_reg_ids.extend(chunk_reg_ids)

#         # C. Prepare Application Data mapped to THIS chunk's Registration IDs
#         apps_data = [
#             {
#                 "application_json": {},
#                 "registration_id": reg_id,
#                 "application_number": f"{offset + i}".zfill(14),
#                 # "application_number": f"APP-{offset + i}-{random_string(5)}",
#                 "type": "",
#                 "registration_type": Registration.RegistrationType.HOST,
#             }
#             for i, reg_id in enumerate(chunk_reg_ids)
#         ]

#         # D. Insert Applications and extend our master list of IDs
#         chunk_app_ids = session.scalars(
#             insert(Application).returning(Application.id),
#             apps_data
#         ).all()
#         all_app_ids.extend(chunk_app_ids)

#     # 3. Flush all chunks to the database within the test transaction
#     session.flush()
#     end_time = time.perf_counter()
#     duration = end_time - start_time

#     # Print the results directly to the console
#     print(f"\n[PROFILER] Inserted {n_records} records in chunks of {chunk_size} "
#           f"-> Time: {duration:.3f} seconds")

#     return {
#         "customer_id": customer.id,
#         "user_id": user.id,
#         "record_count": n_records,
#         "registration_ids": all_reg_ids,
#         "application_ids": all_app_ids,
#     }


@pytest.fixture
def setup_bulk_parents(request, session: Session, random_string, random_integer):

    # Default parameters
    n_records = 10
    chunk_size = 2000  # this is the optimal size discovered in test_perf
    target_days = []  # e.g., [0, 15, 30, 45, 60]
    target_pct = 0.0

    # Extract test-specific parameters if they exist
    if hasattr(request, "param") and isinstance(request.param, dict):
        n_records = request.param.get("records", 10)
        chunk_size = request.param.get("chunk_size", 2000)
        target_days = request.param.get("target_days", [])
        target_pct = request.param.get("target_pct", 0.0)

    # 1. Setup Parents
    customer = User()
    user = User()
    session.add_all([user, customer])
    session.flush()

    now = datetime.now(timezone.utc).date()
    expiry_dates = []

    # Calculate distributions IF targets were passed in
    if target_days and target_pct > 0:
        count_per_target = int(n_records * target_pct)
        remaining_count = n_records - (count_per_target * len(target_days))

        # 1. Generate targeted dates
        for days_out in target_days:
            target_date = now + timedelta(days=days_out)
            expiry_dates.extend([target_date] * count_per_target)

        # 2. Generate noise dates (distribute over 120 days, avoiding targets)
        allowed_noise_days = [d for d in range(120) if d not in target_days]
        for _ in range(remaining_count):
            random_days = random.choice(allowed_noise_days)
            expiry_dates.append(now + timedelta(days=random_days))
    else:
        # Fallback for standard tests: just make everything expire in 1 year
        expiry_dates = [now + timedelta(days=365)] * n_records

    # Shuffle the dates so they are randomized in the database
    random.shuffle(expiry_dates)

    # Lists to hold all generated IDs across all chunks
    all_reg_ids = []
    all_app_ids = []

    start_time = time.perf_counter()

    # 1. Create a reverse mapping so we can translate a 'date' back to the 'days_out' integer
    target_dates_map = {}
    for days_out in target_days:
        target_date = now + timedelta(days=days_out)
        target_dates_map[target_date] = days_out

    # 2. Dictionary to hold our final grouped IDs (e.g., {60: [id1, id2...], 30: [id5, id9...]})
    target_reg_ids = {days_out: [] for days_out in target_days}

    # 2. Loop through the total records in steps of 'chunk_size'
    for offset in range(0, n_records, chunk_size):
        # Handle the last chunk which might be smaller than chunk_size
        current_chunk_size = min(chunk_size, n_records - offset)

        # Grab exactly the dates assigned to this chunk
        chunk_dates = expiry_dates[offset : offset + current_chunk_size]

        # A. Prepare Registration Data for THIS chunk
        regs_data = [
            {
                "registration_type": Registration.RegistrationType.HOST,
                # Use 'offset + i' to ensure uniqueness across all chunks
                "registration_number": "H" + f"{offset + i}".zfill(13),
                "sbc_account_id": random_integer() + offset + i,
                "status": "ACTIVE",
                "user_id": user.id,
                "start_date": now,
                "expiry_date": chunk_dates[i],
            }
            for i in range(current_chunk_size)
        ]

        # B. Insert Registrations and extend our master list of IDs
        chunk_reg_ids = session.scalars(
            insert(Registration).returning(Registration.id), regs_data
        ).all()
        all_reg_ids.extend(chunk_reg_ids)

        # 3. Zip the returned IDs with the dates used to create them
        for reg_id, exp_date in zip(chunk_reg_ids, chunk_dates):
            if exp_date in target_dates_map:
                days_out = target_dates_map[exp_date]
                target_reg_ids[days_out].append(reg_id)

        # C. Prepare Application Data mapped to THIS chunk's Registration IDs
        apps_data = [
            {
                "application_json": {},
                "registration_id": reg_id,
                "application_number": f"{offset + i}".zfill(14),
                # "application_number": f"APP-{offset + i}-{random_string(5)}",
                "type": "",
                "registration_type": Registration.RegistrationType.HOST,
            }
            for i, reg_id in enumerate(chunk_reg_ids)
        ]

        # D. Insert Applications and extend our master list of IDs
        chunk_app_ids = session.scalars(
            insert(Application).returning(Application.id), apps_data
        ).all()
        all_app_ids.extend(chunk_app_ids)

    # 3. Flush all chunks to the database within the test transaction
    session.flush()
    end_time = time.perf_counter()
    duration = end_time - start_time

    # Print the results directly to the console
    print(
        f"\n[PROFILER] Inserted {n_records} records in chunks of {chunk_size} "
        f"-> Time: {duration:.3f} seconds"
    )

    # interaction = CustomerInteraction(
    #     registration_id=1,
    #     channel=ChannelType.EMAIL,
    #     idempotency_key='tning'
    # ).save()

    return {
        "customer_id": customer.id,
        "user_id": user.id,
        "record_count": n_records,
        "registration_ids": all_reg_ids,
        "application_ids": all_app_ids,
        "target_reg_ids": target_reg_ids,
    }
