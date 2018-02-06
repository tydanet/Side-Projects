import Graphics.Gnuplot.Simple

rungeKutta4 :: (Float -> Float -> Float) -> Float -> Float -> Float -> Float -> [(Float, Float)]
rungeKutta4 f y0 t0 tn n = 
    let h = (tn - t0) / n
        rk4 t y vals
            | t >= tn = vals
            | otherwise = 
            let k1 = h * (f t y)
                k2 = h * (f (t + h/2) (y + k1/2))
                k3 = h * (f (t + h/2) (y + k2/2))
                k4 = h * (f (t + h) (y + k3))
                t' = t + h
                y' = y + (k1 + 2*k2 + 2*k3 + k4) / 6
            in rk4 t' y' (vals ++ [(t', y')])
    in rk4 t0 y0 [(t0, y0)]

iv t | (floor t) `mod` 12 == 0 = 1
     | otherwise = 0

f t y = 7*(iv t) - (0.01+0.003125*50)*y

