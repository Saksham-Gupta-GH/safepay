import os
import json
import secrets
import math

KEY_PATH_PRIV = os.path.join(os.path.dirname(__file__), "paillier_priv.json")
KEY_PATH_PUB = os.path.join(os.path.dirname(__file__), "paillier_pub.json")


def _is_prime(n, k=8):
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False
    # Miller-Rabin
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        composite = True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composite = False
                break
        if composite:
            return False
    return True


def _generate_prime(bits=512):
    while True:
        p = secrets.randbits(bits) | 1 | (1 << (bits - 1))
        if _is_prime(p):
            return p


def _lcm(a, b):
    return a // math.gcd(a, b) * b


def _L(u, n):
    return (u - 1) // n


class Paillier:
    def __init__(self, keysize=512):
        self.n = None
        self.nsquare = None
        self.g = None
        self.lambda_param = None
        self.mu = None
        if os.path.exists(KEY_PATH_PRIV) and os.path.exists(KEY_PATH_PUB):
            try:
                self._load_keys()
                return
            except Exception:
                pass
        self._generate_keys(keysize)

    def _generate_keys(self, keysize=512):
        # Generate two primes
        p = _generate_prime(keysize // 2)
        q = _generate_prime(keysize // 2)
        while q == p:
            q = _generate_prime(keysize // 2)

        n = p * q
        nsquare = n * n
        g = n + 1
        lambda_param = _lcm(p - 1, q - 1)

        # compute mu
        x = pow(g, lambda_param, nsquare)
        l = _L(x, n)
        mu = pow(l, -1, n)

        self.n = n
        self.nsquare = nsquare
        self.g = g
        self.lambda_param = lambda_param
        self.mu = mu
        self._save_keys()

    def _save_keys(self):
        pub = {"n": hex(self.n), "g": hex(self.g)}
        priv = {"lambda": hex(self.lambda_param), "mu": hex(self.mu), "n": hex(self.n)}
        with open(KEY_PATH_PUB, "w") as f:
            json.dump(pub, f)
        with open(KEY_PATH_PRIV, "w") as f:
            json.dump(priv, f)

    def _load_keys(self):
        with open(KEY_PATH_PUB, "r") as f:
            pub = json.load(f)
        with open(KEY_PATH_PRIV, "r") as f:
            priv = json.load(f)
        self.n = int(pub["n"], 16)
        self.g = int(pub["g"], 16)
        self.nsquare = self.n * self.n
        self.lambda_param = int(priv["lambda"], 16)
        self.mu = int(priv["mu"], 16)

    def encrypt(self, m: int) -> int:
        """Encrypt an integer m (>=0). Returns ciphertext as integer."""
        if m < 0:
            raise ValueError("Paillier implementation expects non-negative integers for m")
        r = secrets.randbelow(self.n)
        while math.gcd(r, self.n) != 1:
            r = secrets.randbelow(self.n)
        c = (pow(self.g, m, self.nsquare) * pow(r, self.n, self.nsquare)) % self.nsquare
        return c

    def decrypt(self, c: int) -> int:
        x = pow(c, self.lambda_param, self.nsquare)
        l = _L(x, self.n)
        m = (l * self.mu) % self.n
        return m

    def add_ciphertexts(self, c1: int, c2: int) -> int:
        return (c1 * c2) % self.nsquare

    def add_ciphertext_plain(self, c: int, m: int) -> int:
        # c * g^m mod nsquare
        return (c * pow(self.g, m, self.nsquare)) % self.nsquare


# Module-level instance (lazy)
_instance = None


def get_paillier(keysize=512):
    global _instance
    if _instance is None:
        _instance = Paillier(keysize=keysize)
    return _instance
