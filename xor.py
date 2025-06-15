def xor_encrypt(text, key):
    return [ord(c) ^ key for c in text]

s1 = "your_s"
s2 = "al"
s3 = "t_here"

K1 = 0x1A
K2 = 0x2B
K3 = 0x3C

enc_s1 = xor_encrypt(s1, K1)
enc_s2 = xor_encrypt(s2, K2)
enc_s3 = xor_encrypt(s3, K3)

print("const unsigned char s1_a[] = {"+", ".join(str(x) for x in enc_s1)+"};")
print("const unsigned char s2_a[] = {"+", ".join(str(x) for x in enc_s2)+"};")
print("const unsigned char s3_a[] = {"+", ".join(str(x) for x in enc_s3)+"};")
