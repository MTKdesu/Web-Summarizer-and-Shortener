package com.bluewind.shorturl.common.util;

import com.google.common.hash.Hashing;

import java.nio.charset.StandardCharsets;


public class HashUtils {

    private static final char[] CHARS = new char[]{
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    };

    private static final int SIZE = CHARS.length;

    /**
     * 10进制数字转Base62编码
     *
     * @param num
     * @return
     */
    private static String toBase62(long num) {
        StringBuilder sb = new StringBuilder();
        while (num > 0) {
            int i = (int) (num % SIZE);
            sb.append(CHARS[i]);
            num /= SIZE;
        }
        return sb.reverse().toString();
    }

    /**
     * 使用MurmurHash对url进行hash
     * @param str
     * @description 这里使用 Google 出品的 MurmurHash 算法。
     *              MurmurHash 是一种非加密型哈希函数，适用于一般的哈希检索操作。
     *              与其它流行的哈希函数相比，对于规律性较强的 key，MurmurHash 的随机分布特征表现更良好。
     *              非加密意味着着相比 MD5，SHA 这些函数它的性能肯定更高（实际上性能是 MD5 等加密算法的十倍以上）
     * @return hash值的Base62编码
     */
    public static String hashToBase62(String str) {
        int i = Hashing.murmur3_32_fixed().hashString(str, StandardCharsets.UTF_8).asInt();
        long num = i < 0 ? Integer.MAX_VALUE - (long) i : i;
        return toBase62(num);
    }

    public static void main(String[] args) {
        System.out.println(hashToBase62("https://juejin.cn/post/6844904090602848270?share_token=4ba00e67-783a-496a-9b49-fe5cb9b1a4c9"));
    }

}
