from abc import ABC, abstractmethod


class BaseAccount(ABC):
    bank_name = "Vietcombank"

    def __init__(self, account_number, owner_name):
        self.account_number = account_number
        self.owner_name = owner_name
        self.__balance = 0

    @property
    def balance(self):
        return self.__balance

    def _set_balance(self, amount):
        self.__balance = amount

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    def __add__(self, other):
        if not isinstance(other, BaseAccount):
            return NotImplemented

        return self.balance + other.balance

    def __lt__(self, other):
        if not isinstance(other, BaseAccount):
            return NotImplemented

        return self.balance < other.balance

    @staticmethod
    def validate_account_number(account_number):
        return account_number.isdigit() and len(account_number) == 10

    @classmethod
    def update_bank_name(cls, new_name):
        cls.bank_name = new_name

    def display_info(self):
        print("===== THÔNG TIN TÀI KHOẢN =====")
        print(f"Loại tài khoản: {self.__class__.__name__}")
        print(f"Ngân hàng: {self.bank_name}")
        print(f"Số tài khoản: {self.account_number}")
        print(f"Chủ tài khoản: {self.owner_name}")
        print(f"Số dư: {self.balance:,.0f} VND")


class SavingsAccount(BaseAccount):
    def __init__(self, account_number, owner_name, interest_rate):
        super().__init__(account_number, owner_name)
        self.interest_rate = interest_rate

    def deposit(self, amount):
        self._set_balance(self.balance + amount)

    def withdraw(self, amount):
        penalty = amount * 0.02
        total = amount + penalty

        if total > self.balance:
            print("Số dư không đủ")
            return None

        self._set_balance(self.balance - total)
        return penalty

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self._set_balance(self.balance + interest)
        return interest

    def display_info(self):
        super().display_info()
        print(f"Lãi suất: {self.interest_rate * 100:.1f}%")


class CreditAccount(BaseAccount):
    def __init__(self, account_number, owner_name, credit_limit):
        super().__init__(account_number, owner_name)
        self.credit_limit = credit_limit

    def deposit(self, amount):
        self._set_balance(self.balance + amount)

    def withdraw(self, amount):
        credit = self.balance - amount

        if not (credit >= -self.credit_limit):
            print("Vượt quá hạn mức thấu chi cho phép")
            return
        self._set_balance(self.balance - amount)

    def display_info(self):
        super().display_info()
        print(f"Hạn mức tín dụng: {self.credit_limit:,.0f} VND")


class DigitalPremiumMixin:
    def crash_back(self, amount):
        if amount > 5000000:
            reward = amount * 0.01
            self._set_balance(self.balance + reward)


class HybridAccount(SavingsAccount, DigitalPremiumMixin):
    def __init__(self, account_number, owner_name, interest_rate):
        super().__init__(account_number, owner_name, interest_rate)


    def deposit(self, amount):
        refund = amount * 0.01
        self._set_balance(self.balance + amount + refund)
        return refund

    def withdraw(self, amount):
        return super().withdraw(amount)

    def display_info(self):
        super().display_info()


def check_space(message):
    while True:
        info = input(message).strip()

        if info == "":
            print("Không được để trống")
            continue
        return info


def input_float(message):
    while True:
        try:
            info = float(input(message).strip())

            if info < 0:
                print("Vui lòng nhập số >= 0")
                continue
            return info

        except ValueError:
            print("Vui lòng nhập số")


def open_account(accounts, current_account):
    while True:
        sub_choice = input('''
--- CHỌN LOẠI TÀI KHOẢN ---
1. Savings Account (Tài khoản Tiết kiệm)
2. Credit Account (Tài khoản Tín dụng)
3. Hybrid Account (Tài khoản Đa năng)
Chọn loại tài khoản (1-3): ''').strip()

        if not sub_choice in ("1", "2", "3"):
            print("Lựa chọn không hợp lệ, vui lòng nhập 1-3")
            continue
        break

    while True:
        account_number = check_space("Nhập số tài khoản 10 chữ số: ")

        if not BaseAccount.validate_account_number(account_number):
            print("Số tài khoản không hợp lệ! Phải gồm đúng 10 chữ số.")
            continue
        break

    owner_name = check_space("Nhập tên chủ tài khoản: ").upper()

    if sub_choice == "1":
        interest = input_float("Nhập lãi suất năm (ví dụ 0.05): ")
        current_account = SavingsAccount(account_number, owner_name, interest)
        print("Mở tài khoản Tiết kiệm thành công!")

    elif sub_choice == "2":
        limit = input_float("Nhập hạn mức tín dụng: ")
        current_account = CreditAccount(account_number, owner_name, limit)
        print("Mở tài khoản Tín dụng thành công!")

    else:
        interest = input_float("Nhập lãi suất năm (ví dụ 0.05): ")
        current_account = HybridAccount(account_number, owner_name, interest)
        print("Mở tài khoản Đa năng thành công!")

    accounts.append(current_account)
    print(f"Chủ tài khoản: {owner_name}")
    return current_account


def display_acc_info(accounts, current_account):
    if not accounts:
        print("Hệ thống chưa có thông tin tài khoản. Vui lòng mở tài khoản ở Chức năng 1 trước.")
        return

    print("--- THÔNG TIN TÀI KHOẢN HIỆN TẠI ---")
    current_account.display_info()


def make_transaction(accounts, current_account):
    if not accounts:
        print("Hệ thống chưa có thông tin tài khoản. Vui lòng mở tài khoản ở Chức năng 1 trước.")
        return

    while True:
        sub_choice = input('''
--- GIAO DỊCH NẠP / RÚT TIỀN ---
1. Nạp tiền
2. Rút tiền
Chọn giao dịch (1-2): ''').strip()

        if not sub_choice in ("1", "2"):
            print("Lựa chọn không hợp lệ, vui lòng nhập 1 hoặc 2")
            continue
        break

    if sub_choice == "1":
        amount = input_float("Nhập số tiền cần nạp: ")
        if isinstance(current_account, HybridAccount):
            refund = current_account.deposit(amount)
            print(f"[Ưu đãi Premium]: Bạn được hoàn tiền 1% ({refund:,.0f} VND) vào tài khoản!")
            print(f"Số dư mới: {current_account.balance:,.0f} VND")

        else:
            current_account.deposit(amount)
            print(f"Nạp thành công. Số dư: {current_account.balance:,.0f} VND")

    else:
        amount = input_float("Nhập số tiền cần rút: ")
        print("Rút tiền thành công!")
        print(f"Số tiền rút: {amount:,.0f} VND")
        if isinstance(current_account, CreditAccount):
            current_account.withdraw(amount)
            print(f"Số dư còn lại: {current_account.balance:,.0f} VND")

        else:
            penalty = current_account.withdraw(amount)
            if penalty is None:
                return
            print(f"Phí phạt rút trước hạn (2%): {penalty:,.0f} VND")
            print(f"Số dư còn lại: {current_account.balance:,.0f} VND")


def calculate_interest(current_account):
    if current_account is None:
        print("Hệ thống chưa có thông tin tài khoản. Vui lòng mở tài khoản ở Chức năng 1 trước.")
        return

    if isinstance(current_account, CreditAccount):
        print("Tài khoản Tín dụng không được hỗ trợ tính năng này!")
        return
    else:
        print("--- TÍNH LÃI ĐỊNH KỲ ---")
        print(f"Số dư trước tính lãi: {current_account.balance:,.0f} VND")
        print(f"Lãi suất năm: {current_account.interest_rate*100:.1f}%")
        interest = current_account.apply_interest()
        print(f"Tiền lãi nhận được: +{interest:,.0f} VND")
        print(f"Số dư mới sau khi cộng lãi: {current_account.balance:,.0f} VND")


def merging_and_compare(accounts, current_account):
    if len(accounts) < 2: 
        print("Cần ít nhất 2 tài khoản. Vui lòng chọn 1 để mở khóa thêm tài khoản!")
        return
    
    print("--- ĐỒNG BỘ & SO SÁNH TÀI KHOẢN (OPERATOR OVERLOADING) ---")
    print(f"Tài khoản hiện tại (A): {current_account.owner_name} (Số dư: {current_account.balance:,.0f} VND)")
    while True:
        merge_number = check_space("Chọn tài khoản đối ứng (B) từ danh sách hệ thống: ")

        if not BaseAccount.validate_account_number(merge_number):
            print("Số tài khoản không hợp lệ! Phải gồm đúng 10 chữ số.")
            continue
        break

    found = False
    for account in accounts:
        if account.account_number == merge_number:
            found = account
            break

    if not found:
        print("Tài khoản không hợp lệ")
        return

    print(f"\r({found.owner_name} - Số dư: {found.balance:,.0f} VND)")  # \r là ký tự carriage return (đưa con trỏ về đầu dòng hiện tại).

    if current_account < found:
        print("\n[Kết quả So sánh (__lt__)]: Số dư tài khoản A NHỎ HƠN số dư tài khoản B.")
    else:
        print(" [Kết quả So sánh (__lt__)]: Số dư tài khoản A LỚN HƠN số dư tài khoản B.")

    total_balance = current_account + found
    print(f"[Kết quả Tổng hợp (__add__)]: Tổng số tiền sở hữu của cả 2 tài khoản là: {total_balance:,.0f} VND.")


class VNPayGateway:
    def execute_pay(self, account, amount):
        print(f"[Hệ thống VNPay]: Đang kết nối tới tài khoản {account.account_number}...")
        account.withdraw(amount)


class ViettelMoneyGateway:
    def execute_pay(self, account, amount):
        print(f"[Hệ thống Viettel Money]: Đang kết nối tới tài khoản {account.account_number}...")
        account.withdraw(amount)


def process_payment(payment_gateway, account, amount):
    try:
        payment_gateway.execute_pay(account, amount)
        print("Xác thực thanh toán bằng Duck Typing thành công!")
        print(f"Tài khoản đã thanh toán hóa đơn giá trị: {amount:,.0f} VND.")
        print(f"Số dư mới: {account.balance:,.0f} VND.")

    except AttributeError:
        print("Cổng thanh toán không hợp lệ hoặc chưa được tích hợp")

    except ValueError as e:
        print(e)


def make_payment(current_account):
    if current_account is None:
        print("Hệ thống chưa có thông tin tài khoản. Vui lòng mở tài khoản ở Chức năng 1 trước.")
        return
    
    while True:
        sub_choice = input('''
--- THANH TOÁN HÓA ĐƠN QUA CỔNG TRUNG GIAN ---
1. Thanh toán qua VNPay
2. Thanh toán qua Viettel Money
Chọn cổng thanh toán (1-2): ''').strip()
        
        if not sub_choice in ("1", "2"):
            print("Lựa chọn không hợp lệ, vui lòng nhập 1 hoặc 2")
            continue
        break

    amount = input_float("Nhập số tiền hóa đơn: ")

    if sub_choice == "1":
        gateway = VNPayGateway()
    else:
        gateway = ViettelMoneyGateway()

    process_payment(gateway, current_account, amount)


def main():
    accounts = []
    current_account = None

    while True:
        choice = input('''
                       
===== VIETCOMBANK DIGIBANK PRO SIMULATOR =====
1. Mở tài khoản mới (Chọn loại tài khoản)
2. Xem thông tin & Kiểm tra thứ tự kế thừa (MRO)
3. Giao dịch Nạp / Rút tiền & Tính điểm thưởng (Đa hình)
4. Tích lũy / Áp dụng lãi suất định kỳ
5. Kiểm tra tính năng gộp tài khoản & So sánh (Overloading)
6. Thanh toán hóa đơn qua Cổng trung gian (Duck Typing)
7. Thoát chương trình
==============================================
Chọn chức năng (1-7): ''').strip()

        match choice:
            case "1":
                current_account = open_account(accounts, current_account)

            case "2":
                display_acc_info(accounts, current_account)

            case "3":
                make_transaction(accounts, current_account)

            case "4":
                calculate_interest(current_account)

            case "5":
                merging_and_compare(accounts, current_account)

            case "6":
                make_payment(current_account)

            case "7":
                print(
                    "Cảm ơn đã trải nghiệm hệ thống Vietcombank Digibank Pro Simulator!")
                break
            case _:
                print("Lựa chọn không hợp lệ, vui lòng nhập 1-7")


main()