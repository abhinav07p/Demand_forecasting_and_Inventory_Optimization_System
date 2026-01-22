# from datetime import date, timedelta
# import random

# from demand_ops.db.session import get_session
# from demand_ops.db.repositories import ProductRepo, LocationRepo, SalesRepo
# from demand_ops.db.models import SalesDaily


# def seed_demo(days: int = 60):
#     session = get_session()
#     try:
#         p_repo = ProductRepo(session)
#         l_repo = LocationRepo(session)
#         s_repo = SalesRepo(session)

#         p1 = p_repo.upsert("SKU-001", "Milk 1L")
#         p2 = p_repo.upsert("SKU-002", "Bread Loaf")

#         l1 = l_repo.upsert("BOS-01", "Boston Store")
#         l2 = l_repo.upsert("NYC-01", "NYC Store")

#         session.flush()  # ensure IDs exist

#         start = date.today() - timedelta(days=days)
#         for i in range(days):
#             d = start + timedelta(days=i)
#             for (p, l, base, price) in [
#                 (p1, l1, 40, 3.49),
#                 (p1, l2, 55, 3.59),
#                 (p2, l1, 70, 2.99),
#                 (p2, l2, 90, 3.09),
#             ]:
#                 units = max(0, int(random.gauss(base, base * 0.15)))
#                 s_repo.add(
#                     SalesDaily(
#                         product_id=p.id,
#                         location_id=l.id,
#                         sales_date=d,
#                         units_sold=units,
#                         unit_price=price,
#                     )
#                 )

#         session.commit()
#         print("Demo data seeded.")
#     except Exception:
#         session.rollback()
#         raise
#     finally:
#         session.close()


# if __name__ == "__main__":
#     seed_demo()
