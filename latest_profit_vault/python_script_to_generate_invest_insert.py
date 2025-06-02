import random
from datetime import datetime, timedelta

# Sample data extracted from your tables
user_ids = [
    '6553ebd1-a1c6-46af-a000-004d78e9635f',
    'b9fc2372-8437-4f6e-a619-457ece5ff9c4',
    '4176f86a-0a48-45c5-8a24-ea061096271f',
    '5a730d20-6fd4-4aec-b0a1-5e189e2b3c5b',
    '3ba2f8d8-d1ba-43c9-8615-059ca29b04a1',
    '5880d48a-0d72-4975-875b-444b1faaf391',
    '62e05ad8-6e6c-4ee4-9905-50ef776d50b7',
    '452fa2ca-f317-43a3-b9c8-34bc639385ed',
    'a1c3f001-12d4-4a56-b789-111c2b3a4567',
    'b2d4f002-23e5-5b67-c890-222d3c4b5678',
    'c3e5g003-34f6-6c78-d901-333e4d5c6789',
    'd4f6h004-45g7-7d89-e012-444f5e6d7890',
    'e5g7i005-56h8-8e90-f123-555g6f7e8901',
    'f6h8j006-67i9-9f01-a234-666h7g8f9012',
    'g7i9k007-78j0-0g12-b345-777i8h9g0123',
    'h8j0l008-89k1-1h23-c456-888j9i0h1234',
    'i9k1m009-90l2-2i34-d567-999k0j1i2345',
    'j0l2n010-a1m3-3j45-e678-000l1k2j3456',
    '3d328218-c062-44bd-b001-b7cc16f3390c'
]

plans = [
    {
        'plan_id': 'd4f6h004-026A98C1-236F-108C-08FAE0-00E18A276',
        'min_amount': 50,
        'max_amount': 99,
        'monthly_roi': 20
    },
    {
        'plan_id': 'd4f6h004-03E85887-0626-1A52-0CCC27-01D02203C',
        'min_amount': 100,
        'max_amount': 499,
        'monthly_roi': 100
    },
    {
        'plan_id': 'd4f6h004-0566184E-0FEB-2417-015B2E-02BEB9E01',
        'min_amount': 500,
        'max_amount': 999,
        'monthly_roi': 110
    },
    {
        'plan_id': 'd4f6h004-00EDF716-19B1-06CE-052C75-03AD51BC6',
        'min_amount': 1000,
        'max_amount': 4999,
        'monthly_roi': 120
    },
    {
        'plan_id': 'd4f6h004-026BB6DD-2376-1094-08FDBC-00E23CF8C',
        'min_amount': 5000,
        'max_amount': 9999,
        'monthly_roi': 130
    },
    {
        'plan_id': 'd4f6h004-03E976A3-062D-1A59-0CCF03-01D0D4D51',
        'min_amount': 1000,
        'max_amount': 4999,
        'monthly_roi': 140
    },
    {
        'plan_id': 'd4f6h004-0567366A-0FF2-241F-015E0B-02BF6CB17',
        'min_amount': 50000,
        'max_amount': 99999,
        'monthly_roi': 150
    },
    {
        'plan_id': 'd4f6h004-00EF1532-19B8-06D5-052F52-03AE048DC',
        'min_amount': 100000,
        'max_amount': 10000000,
        'monthly_roi': 200
    },
    {
        'plan_id': 'd4f6h004-026CD4F8-237E-109B-090099-00E2EFCA2',
        'min_amount': 1000,
        'max_amount': 4000,
        'monthly_roi': 20
    }
]

def generate_investments():
    sql_statements = []
    for user_id in user_ids:
        num_investments = random.randint(1, 4)
        for _ in range(num_investments):
            plan = random.choice(plans)
            amount = round(random.uniform(plan['min_amount'], plan['max_amount']), 2)
            profit = round((plan['monthly_roi'] / 100) * amount, 2)
            is_active = random.choice([0, 1])
            if is_active:
                start_date = datetime.now() - timedelta(days=random.randint(0, 5))
                end_date = start_date + timedelta(days=30)
            else:
                start_date = datetime.now() - timedelta(days=random.randint(31, 365))
                end_date = start_date + timedelta(days=30)
            created_at = start_date
            sql = f"""INSERT INTO user_investments (user_id, plan_id, amount_invested, profit_earned, start_date, end_date, is_active, created_at)
VALUES ('{user_id}', '{plan['plan_id']}', {amount}, {profit}, '{start_date.strftime('%Y-%m-%d %H:%M:%S')}', '{end_date.strftime('%Y-%m-%d %H:%M:%S')}', {is_active}, '{created_at.strftime('%Y-%m-%d %H:%M:%S')}');"""
            sql_statements.append(sql)
    return sql_statements

# Generate and print the SQL statements
statements = generate_investments()
for stmt in statements:
    print(stmt)
