// 幂运算（非库函数） 使用了欧几里得算法

double Pow(double x, int a)
{
    if (a == 0)
    {
        return 1;
    }
    else if (a == 1)
    {
        return x;
    }
    if (a % 2 == 0)
    {
        return Pow(x * x, a / 2);
    }
    else
    {
        return Pow(x * x, a / 2) * x;
    }
}