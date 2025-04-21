import swisseph as swe
from datetime import datetime, timedelta
from typing import Dict, List
from models.base import Time, GeoLocation, Person
import math

class Calculator:
    # Initialize Swiss Ephemeris
    swe.set_ephe_path()  # Use default ephemeris path

    @staticmethod
    def calculate_planet_positions(time: Time) -> Dict[str, float]:
        """Calculate planet positions at given time"""
        print(f"DEBUG Calculator: Calculating planet positions for time {time.std_time}")
        # Convert time to Julian day
        print(f"DEBUG Calculator: Parsing datetime string: {time.std_time}")
        # Parse full datetime string
        date = datetime.strptime(time.std_time, "%H:%M/%d/%m/%Y/%z")
        print(f"DEBUG Calculator: Parsed datetime: {date}")
        jd = swe.julday(date.year, date.month, date.day, 
                       date.hour + date.minute/60.0)
        print(f"DEBUG Calculator: Converted to Julian Day: {jd}")

        # Calculate for all planets
        planets = {
            'Sun': swe.SUN, 'Moon': swe.MOON, 'Mars': swe.MARS,
            'Mercury': swe.MERCURY, 'Jupiter': swe.JUPITER, 
            'Venus': swe.VENUS, 'Saturn': swe.SATURN,
            'Rahu': swe.MEAN_NODE, 'Ketu': swe.MEAN_NODE
        }

        positions = {}
        for planet_name, planet_id in planets.items():
            if planet_name == 'Ketu':
                # Ketu is 180° opposite to Rahu
                rahu_pos = positions['Rahu']
                positions[planet_name] = (rahu_pos + 180) % 360
            else:
                result = swe.calc_ut(jd, planet_id)[0]
                positions[planet_name] = result[0]  # Longitude

        return positions

    @staticmethod
    def calculate_houses(time: Time) -> Dict[int, float]:
        """Calculate house positions using Placidus system"""
        date = datetime.strptime(time.std_time.split()[0], "%H:%M/%d/%m/%Y")
        jd = swe.julday(date.year, date.month, date.day,
                       date.hour + date.minute/60.0)

        # Calculate houses
        houses = swe.houses(jd, time.location.latitude, 
                          time.location.longitude, b'P')[0]

        return {i+1: pos for i, pos in enumerate(houses)}

    @staticmethod
    def calculate_dasa(birth_time: Time, levels: int = 7) -> Dict[str, Dict]:
        """Calculate Vimshottari dasa periods up to 7 levels (PD1-PD7)"""
        # Define dasa sequence and years
        dasa_sequence = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 
                        'Rahu', 'Jupiter', 'Saturn', 'Mercury']

        # Planet dasa years 
        dasa_years = {
            'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7,
            'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17
        }

        # Get moon position
        moon_pos = Calculator.calculate_planet_positions(birth_time)['Moon']

        # Calculate nakshatra (1-27) based on moon longitude
        nakshatra = math.floor(moon_pos / 13.333333333333334)

        # Calculate remainder within nakshatra
        remainder = (moon_pos % 13.333333333333334) / 13.333333333333334

        # Map nakshatra to starting dasa lord using mod 9
        start_lord_index = nakshatra % 9
        lord = dasa_sequence[start_lord_index]

        # Calculate years remaining in birth dasa
        years = dasa_years[lord]
        initial_years = years * (1 - remainder)

        def get_next_dasa_lord(current_lord: str) -> str:
            """Get next lord in sequence"""
            current_index = dasa_sequence.index(current_lord)
            return dasa_sequence[(current_index + 1) % 9]

        def calculate_sub_period(pd_level: int, main_lord: str, remaining_years: float) -> Dict:
            """Calculate sub periods recursively"""
            if pd_level > levels:
                return None

            lord = main_lord
            total_years = dasa_years[lord]
            sub_period = remaining_years if remaining_years > 0 else total_years

            # Calculate sub-periods (PD2-PD7)
            sub_lords = {}
            if pd_level < levels:
                current_sub_lord = lord
                years_left = sub_period

                while years_left > 0:
                    # Get years for current sub lord
                    lord_total_years = dasa_years[current_sub_lord]
                    lord_years = (lord_total_years / total_years) * sub_period

                    # Calculate next level recursively
                    sub_lords[current_sub_lord] = calculate_sub_period(
                        pd_level + 1, 
                        current_sub_lord,
                        lord_years
                    )

                    # Move to next lord
                    current_sub_lord = get_next_dasa_lord(current_sub_lord)
                    years_left -= lord_years

            return {
                'lord': lord,
                'years': sub_period,
                'sub_periods': sub_lords
            }

        # Calculate main dasa (PD1) and all sub-levels
        start_lord_index = nakshatra % 9
        current_lord = dasa_sequence[start_lord_index]
        initial_years = dasa_years[current_lord] * (1 - remainder)

        dasa_data = calculate_sub_period(1, current_lord, initial_years)

        return {'dasa_periods': dasa_data}

    @staticmethod
    def predict_events(person: Person, start_time: Time, end_time: Time) -> List[Dict]:
        """Predict astrological events for a person in given time range"""
        events = []

        # Get birth chart positions
        birth_positions = Calculator.calculate_planet_positions(person.birth_time)

        # Get positions for prediction period
        current_positions = Calculator.calculate_planet_positions(start_time)

        # Check planetary aspects and transits
        for planet, pos in current_positions.items():
            # Check conjunctions
            for birth_planet, birth_pos in birth_positions.items():
                if abs(pos - birth_pos) < 10:  # Within 10 degrees
                    events.append({
                        'type': 'conjunction',
                        'planets': [planet, birth_planet],
                        'time': start_time.std_time,
                        'description': f"{planet} conjunct natal {birth_planet}"
                    })

        return events

    @staticmethod
    def calculate_moon_longitude(time_str: str, latitude: float, longitude: float) -> float:
        """Placeholder function to calculate moon longitude using location.  Needs implementation."""
        # This is a placeholder; replace with actual calculation using Swiss Ephemeris or similar
        date = datetime.strptime(time_str, "%H:%M/%d/%m/%Y/%z")
        jd = swe.julday(date.year, date.month, date.day, date.hour + date.minute / 60.0)
        pos = swe.calc_ut(jd, swe.MOON)[0]
        return pos[0]


    @staticmethod 
    def calculate_dasa_at_range(birth_time: Time, start_time: Time, end_time: Time, 
                              dasa_system: str = "Vimshottari", 
                              ayanamsa: str = "Raman",
                              levels: int = 3,
                              precision_hours: int = 24) -> Dict[str, List[Dict]]:
        print(f"DEBUG Calculator: Starting dasa calculation with:")
        print(f"DEBUG Calculator: birth_time={birth_time.std_time}")
        print(f"DEBUG Calculator: start_time={start_time.std_time}")
        print(f"DEBUG Calculator: end_time={end_time.std_time}")
        print(f"DEBUG Calculator: dasa_system={dasa_system}")
        print(f"DEBUG Calculator: ayanamsa={ayanamsa}")
        """Calculate dasa periods between start and end time for a person born at birth_time

        Args:
            birth_time: Birth time
            start_time: Start time for prediction
            end_time: End time for prediction 
            dasa_system: Dasa system to use (Vimshottari or Ashtottari)
            ayanamsa: Ayanamsa to use (Raman, Lahiri, KP)
            levels: Number of dasa levels to calculate (1-7)
        """
        # Set ayanamsa
        ayanamsa_flags = {
            "Raman": swe.SIDM_RAMAN,
            "Lahiri": swe.SIDM_LAHIRI,
            "KP": swe.SIDM_KRISHNAMURTI
        }
        selected_ayanamsa = ayanamsa_flags.get(ayanamsa, swe.SIDM_RAMAN)
        print(f"DEBUG Calculator: Setting ayanamsa mode to {selected_ayanamsa}")
        swe.set_sid_mode(selected_ayanamsa)

        # Calculate moon's constellation at birth
        print(f"DEBUG Calculator: Getting moon position for birth time")
        #Using the new function to get moon position
        birth_location = birth_time.location
        moon_pos = Calculator.calculate_moon_longitude(birth_time.std_time, birth_location.latitude, birth_location.longitude)
        print(f"DEBUG Calculator: All planet positions at birth: {moon_pos}")
        # Calculate nakshatra (moon constellation) like C# code
        nakshatra = math.floor(moon_pos / 13.333333)  # 27 nakshatras divided across 360 degrees
        remainder = (moon_pos % 13.333333) / 13.333333  # Get position within nakshatra
        print(f"DEBUG Calculator: Nakshatra: {nakshatra}, Remainder: {remainder}")

        # Define dasa sequences and years first
        dasa_systems = {
            "Vimshottari": {
                "sequence": ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 
                           'Rahu', 'Jupiter', 'Saturn', 'Mercury'],
                "years": {'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10,
                         'Mars': 7, 'Rahu': 18, 'Jupiter': 16, 'Saturn': 19,
                         'Mercury': 17}
            },
            "Ashtottari": {
                "sequence": ['Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 
                           'Saturn', 'Mercury', 'Venus'],
                "years": {'Sun': 6, 'Moon': 15, 'Mars': 8, 'Rahu': 18,
                         'Jupiter': 19, 'Saturn': 10, 'Mercury': 17, 'Venus': 7}
            }
        }

        # Get selected dasa system
        selected_system = dasa_systems.get(dasa_system, dasa_systems["Vimshottari"])
        dasa_sequence = selected_system["sequence"]
        dasa_years = selected_system["years"]

        # Calculate birth dasa planet based on nakshatra
        start_lord_index = nakshatra % 9  # Map to 9 planets cycle
        initial_lord = dasa_sequence[start_lord_index]
        years = dasa_years[initial_lord]
        initial_years = years * (1 - remainder)  # Remaining years in first dasa

        print(f"DEBUG Calculator: Start lord: {initial_lord}, Initial years: {initial_years}")

        # Find start lord index (based on birth nakshatra)
        dasa_periods = []

        # Convert times to datetime for calculations
        print(f"DEBUG Calculator: Parsing birth time: {birth_time.std_time}")
        birth_dt = datetime.strptime(birth_time.std_time, "%H:%M/%d/%m/%Y/%z")
        print(f"DEBUG Calculator: Parsed birth time: {birth_dt}")

        print(f"DEBUG Calculator: Parsing start time: {start_time.std_time}")
        start_dt = datetime.strptime(start_time.std_time, "%H:%M/%d/%m/%Y/%z") 
        print(f"DEBUG Calculator: Parsed start time: {start_dt}")

        print(f"DEBUG Calculator: Parsing end time: {end_time.std_time}")
        end_dt = datetime.strptime(end_time.std_time, "%H:%M/%d/%m/%Y/%z")
        print(f"DEBUG Calculator: Parsed end time: {end_dt}")

        # Calculate dasa progression like C# DasaManager.CurrentDasa8Levels
        # Calculate initial dasa period starting from birth
        initial_years = dasa_years[initial_lord] * (1 - remainder)
        initial_days = initial_years * 365.25

        # Start from birth time and calculate forward
        current_dt = birth_dt
        current_lord_index = start_lord_index

        # Track all periods from birth to end date
        all_periods = []

        # Continue until we pass end date 
        while current_dt < end_dt:
            # Get current period duration
            lord = dasa_sequence[current_lord_index]

            # Calculate period duration
            if lord == initial_lord:
                period_years = initial_years
                initial_years = dasa_years[lord]  # Reset for next occurrence
            else:
                period_years = dasa_years[lord]

            period_days = period_years * 365.25
            period_end = current_dt + timedelta(days=period_days)

            # Only include periods that overlap with requested range
            if period_end > start_dt:
                all_periods.append((current_dt, period_end, lord))

            # Move to next period
            current_dt = period_end
            current_lord_index = (current_lord_index + 1) % len(dasa_sequence)

        # Reset current time to earliest relevant period
        if all_periods:
            current_dt = all_periods[0][0]

        # Generate output for the found periods
        for period_start, period_end, lord in all_periods:
            years = (period_end - period_start).days / 365.25

            # Create period object for overlapping range
            # Calculate exact period using Julian days like C# code
            years_in_days = years * 365.25
            print(f"DEBUG Calculator: Period for lord {lord}:")
            print(f"  Years: {years}")
            print(f"  Days: {years_in_days}")
            print(f"  Start: {current_dt}")
            print(f"  End: {period_end}")
            print(f"  Birth Remainder: {remainder}")
            print(f"  Moon Position: {moon_pos}")
            print(f"  Nakshatra: {nakshatra}")

            if period_end > start_dt:
                # Calculate precise duration in hours
                start = max(current_dt, start_dt)
                end = min(period_end, end_dt)
                duration_hours = (end - start).total_seconds() / 3600
                print(f"  Duration Hours: {duration_hours}")
                start = max(current_dt, start_dt)
                end = min(period_end, end_dt)
                duration_hours = (end - start).total_seconds() / 3600

                # Adjust for ayanamsa
                if selected_ayanamsa == swe.SIDM_LAHIRI:
                    duration_hours += (0.0083333 * duration_hours)

                # Format duration text
                if duration_hours >= 8760:  # 1 year
                    duration_text = f"{duration_hours/8760:.1f} years"
                elif duration_hours >= 720:  # 1 month
                    duration_text = f"{duration_hours/720:.1f} months"
                elif duration_hours >= 24:  # 1 day
                    duration_text = f"{duration_hours/24:.1f} days"
                elif duration_hours >= 1:  # 1 hour
                    duration_text = f"{duration_hours:.1f} hours"
                else:
                    duration_text = f"{duration_hours*60:.1f} minutes"

                def calculate_sub_periods(main_lord, total_duration, start_time, end_time, level=2):
                    if level > levels:
                        return None

                    sub_periods = {}
                    remaining_duration = total_duration
                    sub_lord_index = dasa_sequence.index(main_lord)
                    current_time = start_time

                    while remaining_duration > 0 and current_time < end_time:
                        sub_lord = dasa_sequence[sub_lord_index]
                        # Calculate proportion based on main lord's total years
                        proportion = dasa_years[sub_lord] / sum(dasa_years.values())
                        sub_duration = total_duration * proportion
                        period_end = current_time + timedelta(hours=sub_duration)

                        if sub_duration < 0.001:
                            break

                        sub_period = {
                            'Type': 'Bhukti (Sub Period)' if level == 2 else 'Antaram (Sub-sub Period)' if level == 3 else f'PD{level}',
                            'Start': current_time.strftime("%H:%M %d/%m/%Y %z"),
                            'End': period_end.strftime("%H:%M %d/%m/%Y %z"),
                            'DurationHours': sub_duration,
                            'DurationText': f"{sub_duration/8760:.1f} years",
                            'Lord': sub_lord,
                            'ParentLord': main_lord
                        }

                        if levels > level:
                            sub_sub_periods = calculate_sub_periods(sub_lord, sub_duration, current_time, period_end, level + 1)
                            if sub_sub_periods:
                                sub_period['SubDasas'] = sub_sub_periods

                        sub_periods[sub_lord] = sub_period
                        remaining_duration -= sub_duration
                        current_time = period_end
                        sub_lord_index = (sub_lord_index + 1) % len(dasa_sequence)

                    return sub_periods


                # Create main dasa period with correct formatting
                # Set times to 00:00
                start = start.replace(hour=0, minute=0)
                end = end.replace(hour=0, minute=0)

                period = {
                    'Type': 'Mahadasa (Main Period)', 
                    'Start': start.strftime("%H:%M %d/%m/%Y %z"),
                    'End': end.strftime("%H:%M %d/%m/%Y %z"), 
                    'DurationHours': duration_hours,
                    'DurationText': duration_text,
                    'TechnicalName': f"{lord}PD1",
                    'Lord': lord,
                    'ParentLord': "",
                    'Description': f"Main period of {lord}",
                    'Nature': "Neutral"
                }

                # Calculate sub-periods matching C# implementation
                if levels > 1:
                    sub_periods = calculate_sub_periods(lord, duration_hours, start, end)
                    if sub_periods:
                        period['SubDasas'] = sub_periods

                dasa_periods.append(period)

            current_dt = period_end
            current_lord_index = (current_lord_index + 1) % 9

            # Break if we've gone too far
            if current_dt > end_dt:
                break

        # Sort periods by start time
        dasa_periods.sort(key=lambda x: datetime.strptime(x['Start'], "%H:%M %d/%m/%Y %z"))

        # Format final response
        formatted_periods = {}
        for period in dasa_periods:
            lord = period['Lord']
            formatted_periods[lord] = period

            # Also format SubDasas if they exist
            if 'SubDasas' in period:
                sub_periods = {}
                # Sort sub periods by start time
                sorted_sub_items = sorted(period['SubDasas'].items(), 
                    key=lambda x: datetime.strptime(x[1]['Start'], "%H:%M %d/%m/%Y %z"))
                for sub_lord, sub_period in sorted_sub_items:
                    sub_periods[sub_lord] = sub_period
                period['SubDasas'] = sub_periods

        return {
            'Status': 'Pass',
            'Payload': formatted_periods
        }

    @staticmethod
    def calculate_tarabala(time: Time) -> Dict[str, str]:
        """Calculate Tarabala (auspiciousness of birth lunar day)"""
        # Get moon longitude at birth time
        moon_pos = Calculator.calculate_planet_positions(time)['Moon']

        # Calculate lunar day (1-30)
        lunar_day = math.floor((moon_pos / 12) + 1)

        # Define Tarabala rules
        tarabala_map = {
            1: "Janma (Birth) - Medium",
            2: "Sampat (Wealth) - Excellent", 
            3: "Vipat (Danger) - Bad",
            4: "Kshema (Wellbeing) - Medium",
            5: "Pratyak (Obstacle) - Bad",
            6: "Sadhana (Accomplishment) - Medium",
            7: "Naidhana (Death) - Bad",
            8: "Mitra (Friend) - Excellent",
            9: "ParamaMitra (Great Friend) - Excellent"
        }

        # Get Tarabala index (1-9)
        tarabala_index = ((lunar_day - 1) % 9) + 1

        return {
            'lunar_day': str(lunar_day),
            'tarabala': tarabala_map[tarabala_index]
        }