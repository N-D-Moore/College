function P_A() 
{
    const results = [];
    let nva = 0;
    for (let e = 1; e <= 28; e++) 
    {
        nva++;
        for (let f = 1; f <= 28; f++) 
        {
            nva++;
            const d = e + f + 21;
            const a = (d * d - 417) / (e * e);
            const mod = (d * d - 417) % (e * e);
            if (a > e + f && mod === 0 && a >= 1 && a <= 50 && d >= 1 && d <= 50)
            {
                for (let b = 1; b <= 47; b++)
                {
                    nva++;
                    const c = a - b - e - f;
                    if (c >= 1 && c <= 50)
                    {
                        results.push([a, b, c, d, e, f]);
                    }
                }
            }
        }
    }
    return{
        nva,
        data: results
    };
}
function P_B(nva, inputs)
{
    const results = [];
    for (let idx = 0; idx < inputs.length; idx++)
    {
        const [a, b, c, d, e, f] = inputs[idx];
        const g = f - Math.sqrt(a + d + 1);
        const f2 = (Math.pow(g - c, 2) - 1) / (c * c);
        if (f2 === f)
        {
            const j = (g * g + 39) / 4;
            for (let i = 1; i <= 50; i++)
            {
                nva++;
                const h = (Math.pow(g + i, 2) - e * 12) / j;
                const c8 = Math.pow(i - g, 9) === Math.pow(f - h, 3);
                if (c8)
                {
                    results.push([a, b, c, d, e, f, g, h, i, j]);
                }
            }
        }
    }
    return{
        nva,
        data: results
    };
}
function P_C(nva, inputs)
{
    const results = [];
    for (let idx = 0; idx < inputs.length; idx++)
    {
        const [a, b, c, d, e, f, g, h, i, j] = inputs[idx];
        const o = Math.sqrt(g * h * i * b + 133);
        for (let n = 1; n <= 50; n++)
        {
            nva++;
            const isGoodN = Math.pow(n, 3) - 3 * n * o * (n - o) - (f - i) * n - Math.pow(o, 3) + 7 === 0;
            if (isGoodN)
            {
                const m = Math.sqrt(n * n - 291);
                const k = Math.sqrt(2 * m + 6);
                for (let l = 0; l <= 50; l++)
                {
                    nva++;
                    const isGoodL = Math.pow(l, 3) - (l + b) * k + i === 0;
                    if (isGoodL)
                    {
                        results.push([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]);
                        return{
                            nva,
                            data: results
                        };
                    }
                }
            }
        }
    }
    return{
        nva,
        data: results
    };
}

function printResults(nva, results)
{
    if (results.length)
    {
        for (let idx = 0; idx < results.length; idx++)
        {
            const result = results[idx];
            console.log(result.join(","));
        }
    }
    else
    {
        console.log("No solution exists");
    }
    console.log("nva: ", nva);
}

let resultA = P_A();
printResults(resultA.nva, resultA.data);
let resultB = P_B(resultA.nva, resultA.data);
printResults(resultB.nva, resultB.data);
let resultC = P_C(resultB.nva, resultB.data);
printResults(resultC.nva, resultC.data);