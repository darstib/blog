// 求最大公因数（非库函数）

int gcd(int m, int n)
{
    if (m == n)
    {
        return m;
    }
    else if (m < n)
    {
        int t = m;
        m = n;
        n = t;
    }
    while (n != 0)
    {
        int re = m % n;
        m = n;
        n = re;
    }
    return m;
}