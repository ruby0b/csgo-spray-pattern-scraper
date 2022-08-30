Scrapes [csweapons.com](https://www.csweapons.com/) for all fixed CS:GO spray patterns and saves them as `pitch,yaw`[^1] CSV files (see the `out/` folder for the results).

I needed the data to implement the spray patterns myself and this seemed like the easiest approach I could find.

This method obviously relies on the accuracy of csweapons.com's data. It also translates their SVG data kinda sloppily by assuming that -60 y coordinates are equivalent to an angle of -12 degrees (the reference point I used was the pitch of the highest AK-47 shot in its pattern).

[^1]: The pitch and yaw are both inverted because that's how they seem to work in source engine games. So a negative pitch means looking upwards and a negative yaw means looking further right.