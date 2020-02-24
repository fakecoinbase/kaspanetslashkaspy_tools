# Copyright (c) 2019 Pieter Wuille
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test-only secp256k1 elliptic curve implementation

WARNING: This code is slow, uses bad randomness, does not properly protect
keys, and is trivially vulnerable to side channel attacks. Do not use for
anything but tests."""
import random
from hashlib import sha256


def modinv(a, n):
    """Compute the modular inverse of a modulo n

    See https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Modular_integers.
    """
    t1, t2 = 0, 1
    r1, r2 = n, a
    while r2 != 0:
        q = r1 // r2
        t1, t2 = t2, t1 - q * t2
        r1, r2 = r2, r1 - q * r2
    if r1 > 1:
        return None
    if t1 < 0:
        t1 += n
    return t1


def jacobi_symbol(n, k):
    """Compute the Jacobi symbol of n modulo k

    See http://en.wikipedia.org/wiki/Jacobi_symbol

    For our application k is always prime, so this is the same as the Legendre symbol."""
    assert k > 0 and k & 1, "jacobi symbol is only defined for positive odd k"
    n %= k
    t = 0
    while n != 0:
        while n & 1 == 0:
            n >>= 1
            r = k & 7
            t ^= (r == 3 or r == 5)
        n, k = k, n
        t ^= (n & k & 3 == 3)
        n = n % k
    if k == 1:
        return -1 if t else 1
    return 0


def modsqrt(a, p):
    """Compute the square root of a modulo p when p % 4 = 3.

    The Tonelli-Shanks algorithm can be used. See https://en.wikipedia.org/wiki/Tonelli-Shanks_algorithm

    Limiting this function to only work for p % 4 = 3 means we don't need to
    iterate through the loop. The highest n such that p - 1 = 2^n Q with Q odd
    is n = 1. Therefore Q = (p-1)/2 and sqrt = a^((Q+1)/2) = a^((p+1)/4)

    secp256k1's is defined over field of size 2**256 - 2**32 - 977, which is 3 mod 4.
    """
    if p % 4 != 3:
        raise NotImplementedError("modsqrt only implemented for p % 4 = 3")
    sqrt = pow(a, (p + 1) // 4, p)
    if pow(sqrt, 2, p) == a % p:
        return sqrt
    return None


class EllipticCurve:
    def __init__(self, p, a, b):
        """Initialize elliptic curve y^2 = x^3 + a*x + b over GF(p)."""
        self.p = p
        self.a = a % p
        self.b = b % p

    def affine(self, p1):
        """Convert a Jacobian point tuple p1 to affine form, or None if at infinity.

        An affine point is represented as the Jacobian (x, y, 1)"""
        x1, y1, z1 = p1
        if z1 == 0:
            return None
        inv = modinv(z1, self.p)
        inv_2 = (inv ** 2) % self.p
        inv_3 = (inv_2 * inv) % self.p
        return ((inv_2 * x1) % self.p, (inv_3 * y1) % self.p, 1)

    def has_square_y(self, p1):
        """Whether the point p1 has a Y coordinate that is a quadratic residue when expressed in affine coordinates.
        An integer is a quadratic residue modulo a prime if its Jacobi symbol modulo that prime is 1.
        To convert to affine from Jacobian coordinates, the Y coordinate is p[1] * p[2]^-3 (see the affine()
        function above). Since the ratio of p[2] to p[2]^-3 is p[2]^4, which is a square, we instead
        check the Jacobi symbol of p[1] * p[2], avoiding costly inverses and multiplications."""
        return jacobi_symbol(p1[1] * p1[2], SECP256K1_FIELD_SIZE) == 1

    def negate(self, p1):
        """Negate a Jacobian point tuple p1."""
        x1, y1, z1 = p1
        return (x1, (self.p - y1) % self.p, z1)

    def on_curve(self, p1):
        """Determine whether a Jacobian tuple p is on the curve (and not infinity)"""
        x1, y1, z1 = p1
        z2 = pow(z1, 2, self.p)
        z4 = pow(z2, 2, self.p)
        return z1 != 0 and (pow(x1, 3, self.p) + self.a * x1 * z4 + self.b * z2 * z4 - pow(y1, 2, self.p)) % self.p == 0

    def is_x_coord(self, x):
        """Test whether x is a valid X coordinate on the curve."""
        x_3 = pow(x, 3, self.p)
        return jacobi_symbol(x_3 + self.a * x + self.b, self.p) != -1

    def lift_x(self, x):
        """Given an X coordinate on the curve, return a corresponding affine point."""
        x_3 = pow(x, 3, self.p)
        v = x_3 + self.a * x + self.b
        y = modsqrt(v, self.p)
        if y is None:
            return None
        return (x, y, 1)

    def double(self, p1):
        """Double a Jacobian tuple p1

        See https://en.wikibooks.org/wiki/Cryptography/Prime_Curve/Jacobian_Coordinates - Point Doubling"""
        x1, y1, z1 = p1
        if z1 == 0:
            return (0, 1, 0)
        y1_2 = (y1 ** 2) % self.p
        y1_4 = (y1_2 ** 2) % self.p
        x1_2 = (x1 ** 2) % self.p
        s = (4 * x1 * y1_2) % self.p
        m = 3 * x1_2
        if self.a:
            m += self.a * pow(z1, 4, self.p)
        m = m % self.p
        x2 = (m ** 2 - 2 * s) % self.p
        y2 = (m * (s - x2) - 8 * y1_4) % self.p
        z2 = (2 * y1 * z1) % self.p
        return (x2, y2, z2)

    def add_mixed(self, p1, p2):
        """Add a Jacobian tuple p1 and an affine tuple p2

        See https://en.wikibooks.org/wiki/Cryptography/Prime_Curve/Jacobian_Coordinates - Point Addition (with affine point)"""
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        assert (z2 == 1)
        # Adding to the point at infinity is a no-op
        if z1 == 0:
            return p2
        z1_2 = (z1 ** 2) % self.p
        z1_3 = (z1_2 * z1) % self.p
        u2 = (x2 * z1_2) % self.p
        s2 = (y2 * z1_3) % self.p
        if x1 == u2:
            if (y1 != s2):
                # p1 and p2 are inverses. Return the point at infinity.
                return (0, 1, 0)
            # p1 == p2. The formulas below fail when the two points are equal.
            return self.double(p1)
        h = u2 - x1
        r = s2 - y1
        h_2 = (h ** 2) % self.p
        h_3 = (h_2 * h) % self.p
        u1_h_2 = (x1 * h_2) % self.p
        x3 = (r ** 2 - h_3 - 2 * u1_h_2) % self.p
        y3 = (r * (u1_h_2 - x3) - y1 * h_3) % self.p
        z3 = (h * z1) % self.p
        return (x3, y3, z3)

    def add(self, p1, p2):
        """Add two Jacobian tuples p1 and p2

        See https://en.wikibooks.org/wiki/Cryptography/Prime_Curve/Jacobian_Coordinates - Point Addition"""
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        # Adding the point at infinity is a no-op
        if z1 == 0:
            return p2
        if z2 == 0:
            return p1
        # Adding an Affine to a Jacobian is more efficient since we save field multiplications and squarings when z = 1
        if z1 == 1:
            return self.add_mixed(p2, p1)
        if z2 == 1:
            return self.add_mixed(p1, p2)
        z1_2 = (z1 ** 2) % self.p
        z1_3 = (z1_2 * z1) % self.p
        z2_2 = (z2 ** 2) % self.p
        z2_3 = (z2_2 * z2) % self.p
        u1 = (x1 * z2_2) % self.p
        u2 = (x2 * z1_2) % self.p
        s1 = (y1 * z2_3) % self.p
        s2 = (y2 * z1_3) % self.p
        if u1 == u2:
            if (s1 != s2):
                # p1 and p2 are inverses. Return the point at infinity.
                return (0, 1, 0)
            # p1 == p2. The formulas below fail when the two points are equal.
            return self.double(p1)
        h = u2 - u1
        r = s2 - s1
        h_2 = (h ** 2) % self.p
        h_3 = (h_2 * h) % self.p
        u1_h_2 = (u1 * h_2) % self.p
        x3 = (r ** 2 - h_3 - 2 * u1_h_2) % self.p
        y3 = (r * (u1_h_2 - x3) - s1 * h_3) % self.p
        z3 = (h * z1 * z2) % self.p
        return (x3, y3, z3)

    def mul(self, ps):
        """Compute a (multi) point multiplication

        ps is a list of (Jacobian tuple, scalar) pairs.
        """
        r = (0, 1, 0)
        for i in range(255, -1, -1):
            r = self.double(r)
            for (p, n) in ps:
                if ((n >> i) & 1):
                    r = self.add(r, p)
        return r


SECP256K1_FIELD_SIZE = 2 ** 256 - 2 ** 32 - 977
SECP256K1 = EllipticCurve(SECP256K1_FIELD_SIZE, 0, 7)
SECP256K1_G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
               0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8, 1)
SECP256K1_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
SECP256K1_ORDER_HALF = SECP256K1_ORDER // 2


class ECPubKey():
    """A secp256k1 public key"""

    def __init__(self):
        """Construct an uninitialized public key"""
        self.valid = False

    def set(self, data):
        """Construct a public key from a serialization in compressed or uncompressed format"""
        if (len(data) == 65 and data[0] == 0x04):
            p = (int.from_bytes(data[1:33], 'big'), int.from_bytes(data[33:65], 'big'), 1)
            self.valid = SECP256K1.on_curve(p)
            if self.valid:
                self.p = p
                self.compressed = False
        elif (len(data) == 33 and (data[0] == 0x02 or data[0] == 0x03)):
            x = int.from_bytes(data[1:33], 'big')
            if SECP256K1.is_x_coord(x):
                p = SECP256K1.lift_x(x)
                # if the oddness of the y co-ord isn't correct, find the other
                # valid y
                if (p[1] & 1) != (data[0] & 1):
                    p = SECP256K1.negate(p)
                self.p = p
                self.valid = True
                self.compressed = True
            else:
                self.valid = False
        else:
            self.valid = False

    @property
    def is_compressed(self):
        return self.compressed

    @property
    def is_valid(self):
        return self.valid

    def get_bytes(self):
        assert (self.valid)
        p = SECP256K1.affine(self.p)
        if p is None:
            return None
        if self.compressed:
            return bytes([0x02 + (p[1] & 1)]) + p[0].to_bytes(32, 'big')
        else:
            return bytes([0x04]) + p[0].to_bytes(32, 'big') + p[1].to_bytes(32, 'big')

    def verify_schnorr(self, sig, msg):
        """ Verify a Schnorr signature the same as Kaspad Go implementation """
        assert (self.valid)
        assert (len(sig) == 64)
        assert (len(msg) == 32)
        # Input validation.
        rx = int.from_bytes(sig[0:32], 'big')
        if rx >= SECP256K1_FIELD_SIZE:
            return False
        s = int.from_bytes(sig[32:64], 'big')
        if s >= SECP256K1_ORDER:
            return False

        P = SECP256K1.affine(self.p)
        P_compressed = bytes([0x02 + (P[1] & 1)]) + P[0].to_bytes(32, 'big')

        e = int.from_bytes(sha256(sig[0:32] + P_compressed + msg).digest(), 'big') % SECP256K1_ORDER
        R = SECP256K1.mul([(SECP256K1_G, s), (P, SECP256K1_ORDER - e)])
        # R_y must have Jacobi symbol of 1 to be valid
        if not SECP256K1.has_square_y(R):
            return False
        # Check that R_x is equal to the inputted Rx
        if ((rx * R[2] * R[2]) % SECP256K1_FIELD_SIZE) != R[0]:
            return False
        return True


class ECKey():
    """A secp256k1 private key"""

    def __init__(self):
        self.valid = False

    def set(self, secret, compressed):
        """Construct a private key object with given 32-byte secret and compressed flag."""
        assert (len(secret) == 32)
        secret = int.from_bytes(secret, 'big')
        self.valid = (secret > 0 and secret < SECP256K1_ORDER)
        if self.valid:
            self.secret = secret
            self.compressed = compressed

    def generate(self, compressed=True):
        """Generate a random private key (compressed or uncompressed)."""
        self.set(random.randrange(1, SECP256K1_ORDER).to_bytes(32, 'big'), compressed)

    def get_bytes(self):
        """Retrieve the 32-byte representation of this key."""
        assert (self.valid)
        return self.secret.to_bytes(32, 'big')

    @property
    def is_valid(self):
        return self.valid

    @property
    def is_compressed(self):
        return self.compressed

    def get_pubkey(self):
        """Compute an ECPubKey object for this secret key."""
        assert (self.valid)
        ret = ECPubKey()
        p = SECP256K1.mul([(SECP256K1_G, self.secret)])
        ret.p = p
        ret.valid = True
        ret.compressed = self.compressed
        return ret

    def sign_schnorr(self, msg):
        """Create a Schnorr signature the same as Kaspad Go implementation"""
        assert (self.valid)
        assert (len(msg) == 32)

        d = self.secret
        if d >= SECP256K1_ORDER:
            return None
        P = SECP256K1.affine(SECP256K1.mul([(SECP256K1_G, d)]))
        P_compressed = bytes([0x02 + (P[1] & 1)]) + P[0].to_bytes(32, 'big')

        # Use random nonce, because current Go implementation uses RFC6979 and future one might use BIP-340.
        kp = random.randrange(1, SECP256K1_ORDER)
        R = SECP256K1.affine(SECP256K1.mul([(SECP256K1_G, kp)]))
        Rx = R[0].to_bytes(32, 'big')
        # Negate if jacobi symbol is -1.
        k = kp if SECP256K1.has_square_y(R) else SECP256K1_ORDER - kp

        e = int.from_bytes(sha256(Rx + P_compressed + msg).digest(), 'big') % SECP256K1_ORDER
        s = (k + e * d) % SECP256K1_ORDER
        return Rx + s.to_bytes(32, 'big')


key = ECKey()
key.generate()
msg = sha256(b'msg').digest()
sig = key.sign_schnorr(msg)
pubkey = key.get_pubkey()
assert pubkey.verify_schnorr(sig, msg)
print(
    "msg: {} privkey: {}. pubkey: {}. signature: {}".format(msg.hex(), key.get_bytes().hex(), pubkey.get_bytes().hex(),
                                                            sig.hex()))
