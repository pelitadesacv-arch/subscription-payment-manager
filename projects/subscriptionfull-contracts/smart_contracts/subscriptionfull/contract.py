from algopy import ARC4Contract, String, UInt64, Bytes, Global, Txn, gtxn
from algopy.arc4 import abimethod, Bool, UInt64 as ARC4UInt64, Address as ARC4Address


class SubscriptionPaymentManager(ARC4Contract):
    """
    Smart contract sederhana untuk mengelola pembayaran berlangganan.
    Siap digunakan dan di-deploy ke Algorand.
    """
    
    def __init__(self) -> None:
        # Inisialisasi variabel global
        self.total_subscriptions = UInt64(0)
    
    
    @abimethod()
    def hello(self, name: String) -> String:
        """Method hello sederhana untuk testing"""
        return "Hello, " + name
    
    
    @abimethod(create="require")
    def create_app(self) -> String:
        """Dipanggil saat contract pertama kali di-deploy"""
        self.total_subscriptions = UInt64(0)
        return String("Subscription Manager deployed successfully!")
    
    
    @abimethod()
    def create_subscription(self, amount: ARC4UInt64, interval_days: ARC4UInt64) -> String:
        """
        Buat subscription baru.
        
        Args:
            amount: Jumlah pembayaran dalam microAlgos (1 ALGO = 1000000 microAlgos)
            interval_days: Interval pembayaran dalam hari (contoh: 30 untuk bulanan)
        
        Returns:
            Pesan konfirmasi
        """
        # Konversi dari ARC4 ke native
        amount_native = amount.native
        interval_native = interval_days.native
        
        # Validasi input
        assert amount_native > UInt64(0), "Amount must be greater than 0"
        assert interval_native > UInt64(0), "Interval must be greater than 0"
        
        # Simpan data ke box storage dengan key = alamat pengguna
        box_key = Txn.sender.bytes
        
        # Format data: amount (8 bytes) + interval_days (8 bytes) + last_payment (8 bytes) + is_active (1 byte)
        current_time = Global.latest_timestamp
        interval_seconds = interval_native * UInt64(86400)  # Convert days to seconds
        
        # Pack data sebagai bytes
        data = amount_native.bytes + interval_seconds.bytes + current_time.bytes + Bytes(b"\x01")
        
        # Simpan ke box storage
        self.box_create(box_key, UInt64(25))  # 8+8+8+1 = 25 bytes
        self.box_put(box_key, data)
        
        # Increment total subscriptions
        self.total_subscriptions += UInt64(1)
        
        return String("Subscription created! Amount: " + String.from_bytes(amount_native.bytes))
    
    
    @abimethod()
    def get_subscription_info(self) -> String:
        """
        Lihat info subscription milik pengguna.
        
        Returns:
            Info subscription dalam format string
        """
        box_key = Txn.sender.bytes
        
        # Check apakah box exists
        box_exists = self.box_length(box_key)
        
        if box_exists == UInt64(0):
            return String("No subscription found for this address")
        
        # Ambil data dari box
        data = self.box_get(box_key)
        
        # Parse data (simplified - return raw confirmation)
        return String("Subscription found! Use check_payment_due to see status")
    
    
    @abimethod()
    def check_payment_due(self) -> Bool:
        """
        Cek apakah pembayaran sudah jatuh tempo.
        
        Returns:
            True jika pembayaran sudah jatuh tempo, False jika belum
        """
        box_key = Txn.sender.bytes
        
        # Check apakah subscription exists
        box_length = self.box_length(box_key)
        if box_length == UInt64(0):
            return Bool(False)
        
        # Ambil data
        data = self.box_get(box_key)
        
        # Extract last_payment timestamp (bytes 16-24)
        last_payment_bytes = data[16:24]
        last_payment = UInt64.from_bytes(last_payment_bytes)
        
        # Extract interval (bytes 8-16)
        interval_bytes = data[8:16]
        interval = UInt64.from_bytes(interval_bytes)
        
        # Extract is_active flag (byte 24)
        is_active_byte = data[24:25]
        is_active = is_active_byte == Bytes(b"\x01")
        
        if not is_active:
            return Bool(False)
        
        # Check if payment is due
        next_payment_time = last_payment + interval
        current_time = Global.latest_timestamp
        
        return Bool(current_time >= next_payment_time)
    
    
    @abimethod()
    def cancel_subscription(self) -> String:
        """
        Cancel subscription.
        
        Returns:
            Pesan konfirmasi
        """
        box_key = Txn.sender.bytes
        
        # Check apakah subscription exists
        if self.box_length(box_key) == UInt64(0):
            return String("No active subscription found")
        
        # Ambil data existing
        data = self.box_get(box_key)
        
        # Update is_active flag menjadi 0 (inactive)
        new_data = data[:24] + Bytes(b"\x00")
        self.box_put(box_key, new_data)
        
        return String("Subscription cancelled successfully!")
    
    
    @abimethod()
    def get_total_subscriptions(self) -> ARC4UInt64:
        """
        Lihat total subscription yang pernah dibuat.
        
        Returns:
            Total subscription
        """
        return ARC4UInt64(self.total_subscriptions)
    
    
    @abimethod()
    def delete_subscription(self) -> String:
        """
        Hapus subscription dari storage (untuk free up space).
        
        Returns:
            Pesan konfirmasi
        """
        box_key = Txn.sender.bytes
        
        if self.box_length(box_key) == UInt64(0):
            return String("No subscription to delete")
        
        # Hapus box
        self.box_delete(box_key)
        
        return String("Subscription deleted successfully!")

