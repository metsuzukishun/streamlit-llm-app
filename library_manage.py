from datetime import datetime, timedelta

books = []
members = []
borrow_records = []

def add_book(book_id, title, author, copies):
    for book in books:
        if book["book_id"] == book_id:
            print(f"図書ID「{book_id}」の本は既に存在します。")
            return

    books.append({"book_id": book_id, "title": title, "author": author, "copies": copies, "available_copies": copies})
    print(f"図書「{title}」（ID: {book_id}, 著者: {author}, 冊数: {copies}）を追加しました。")

def list_books():
    if not books:
        print("現在、登録されている図書はありません。")
        return

    print("--- 図書一覧 ---")
    for book in books:
        print(f"ID: {book['book_id']}, タイトル: {book['title']}, 著者: {book['author']}, 総冊数: {book['copies']}, 在庫: {book['available_copies']}")

def search_book(book_id):
    for book in books:
        if book["book_id"] == book_id:
            print(f"ID: {book['book_id']}, タイトル: {book['title']}, 著者: {book['author']}, 総冊数: {book['copies']}, 在庫: {book['available_copies']}")
            return
    print(f"図書ID「{book_id}」の本は存在しません。")

def add_member(member_id, name):
    for member in members:
        if member["member_id"] == member_id:
            print(f"会員ID「{member_id}」の会員は既に存在します。")
            return

    members.append({"member_id": member_id, "name": name})
    print(f"会員「{name}」（ID: {member_id}）を追加しました。")

def list_members():
    if not members:
        print("現在、登録されている会員はいません。")
        return

    print("--- 会員一覧 ---")
    for member in members:
        print(f"ID: {member['member_id']}, 名前: {member['name']}")

def borrow_book(book_id, member_id):
    book = ""
    for b in books:
        if b["book_id"] == book_id:
            book = b
            break
    if not book:
        print(f"図書ID「{book_id}」の本は存在しません。")
        return

    member = ""
    for m in members:
        if m["member_id"] == member_id:
            member = m
            break
    if not member:
        print(f"会員ID「{member_id}」の会員は存在しません。")
        return

    if book["available_copies"] <= 0:
        print(f"図書「{book['title']}」は現在貸出可能な冊数がありません。")
        return

    record_count = 0
    for record in borrow_records:
        if member["member_id"] == record["member_id"]:
            record_count += 1
    if record_count == 5:
        print(f"貸出可能数は5冊までです。")
        return

    borrow_records.append({
        "book_id": book_id,
        "member_id": member_id,
        "borrow_date": "2024-11-24",
        "due_date": "2024-12-01",
        "returned": False
    })
    print(f"図書「{book['title']}」を会員「{member['name']}」に貸し出しました。\n返却期限: 2024-12-01")

    book["available_copies"] -= 1

def list_borrowed_books():
    print("--- 貸出中の図書一覧 ---")
    borrow_count = 0
    for record in borrow_records:
        if not record["returned"]:
            book = ""
            for b in books:
                if b["book_id"] == record["book_id"]:
                    book = b
            member = ""
            for m in members:
                if m["member_id"] == record["member_id"]:
                    member = m
            print(f"図書: {book['title']}（ID: {record['book_id']}）, 会員: {member['name']}（ID: {record['member_id']}）, 貸出日: {record['borrow_date']}, 返却期限: {record['due_date']}")
            borrow_count += 1
    if borrow_count == 0:
        print("現在、貸出中の図書はありません。")

def return_book(book_id, member_id):
    record = ""
    for r in borrow_records:
        if r["book_id"] == book_id and r["member_id"] == member_id and not r["returned"]:
            r["returned"] = True
            record = r
            break
    if not record:
        print(f"図書ID「{book_id}」本を会員ID「{member_id}」の会員は借りていません。")
        return

    book = ""
    for b in books:
        if b["book_id"] == book_id:
            b["available_copies"] += 1
            book = b
            break

    if not book:
        print(f"図書ID「{book['book_id']}」の本は存在しません。")
        return
    print(f"図書「{book['title']}」が返却されました。")

def calculate_fines():
    print("--- 延滞料金一覧 ---")
    borrow_count = 0
    for record in borrow_records:
        if not record["returned"]:
            book = ""
            for b in books:
                if b["book_id"] == record["book_id"]:
                    book = b
                    break
            member = ""
            for m in members:
                if m["member_id"] == record["member_id"]:
                    member = m
                    break
            due_date = "2024-12-01"
            today = "2024-12-24"
            overdue_days = max((int(today[-2:]) - int(due_date[-2:])), 0)
            fine = overdue_days * 100
            print(f"図書: {book['title']}（ID: {record['book_id']}）, 会員: {member['name']}（ID: {record['member_id']}）, 延滞料金: {fine}円")
    if borrow_count == 0:
        print("現在、貸出中の図書はありません。")

def extend_due_date(book_id, member_id, extra_days):
    """
    指定された図書と会員の貸出期限を延長する関数。
    extra_days: 延長する日数。
    """
    for record in borrow_records:
        if record["book_id"] == book_id and record["member_id"] == member_id and not record["returned"]:
            old_due_date = record["due_date"]
            year, month, day = map(int, old_due_date.split("-"))
            day += extra_days
            # 簡易的な日付計算（実際にはdatetimeモジュールを使うべき）
            if day > 30:  # 仮に30日を1ヶ月とする
                day -= 30
                month += 1
            if month > 12:
                month -= 12
                year += 1
            record["due_date"] = f"{year:04d}-{month:02d}-{day:02d}"
            print(f"貸出期限が延長されました: {old_due_date} → {record['due_date']}")
            return
    print("指定された図書または会員が見つからないか、既に返却されています。")

def find_item_by_key(items, key, value):
    """
    汎用的な検索関数。リスト内の辞書からキーと値が一致する最初のアイテムを返す。
    """
    return next((item for item in items if item[key] == value), None)

def calculate_overdue_fine(due_date, return_date=None):
    """
    延滞料金を計算する関数。
    1日あたり100円の延滞料金を計算。
    """
    if return_date is None:
        return_date = datetime.now().date()
    overdue_days = (return_date - due_date).days
    return max(overdue_days * 100, 0) if overdue_days > 0 else 0

def main():
    while True:
        print("図書館管理システムメニュー:")
        print("1: 図書を追加")
        print("2: 図書一覧を表示")
        print("3: 図書を検索")
        print("4: 会員を追加")
        print("5: 会員一覧を表示")
        print("6: 図書を貸し出す")
        print("7: 貸出中の図書一覧を表示")
        print("8: 図書を返却")
        print("9: 延滞料金を計算")
        print("10: 貸出期限を延長")
        print("11: 終了")

        try:
            choice = int(input("操作を選択してください（1-11）: "))

            if choice == 1:
                book_id = input("図書IDを入力してください: ")
                title = input("タイトルを入力してください: ")
                author = input("著者名を入力してください: ")
                copies = int(input("冊数を入力してください: "))
                add_book(book_id, title, author, copies)

            elif choice == 2:
                list_books()

            elif choice == 3:
                book_id = input("検索する図書IDを入力してください: ")
                search_book(book_id)

            elif choice == 4:
                member_id = input("会員IDを入力してください: ")
                name = input("名前を入力してください: ")
                add_member(member_id, name)

            elif choice == 5:
                list_members()

            elif choice == 6:
                book_id = input("貸し出す図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                borrow_book(book_id, member_id)

            elif choice == 7:
                list_borrowed_books()

            elif choice == 8:
                book_id = input("返却する図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                return_book(book_id, member_id)

            elif choice == 9:
                calculate_fines()

#　GitHub Copilotの提案を受け、新規機能として関数を1つ追加してください。で追加した関数
            elif choice == 10:
                book_id = input("延長する図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                extra_days = int(input("延長する日数を入力してください: "))
                extend_due_date(book_id, member_id, extra_days)

            elif choice == 11:
                print("図書館管理システムを終了します。")
                break

            else:
                print("無効な選択です。1-11の数字を入力してください。")

        except ValueError as e:
            print(f"入力エラー: {e}")
        except Exception as e:
            print(f"予期しないエラーが発生しました: {e}")

main()