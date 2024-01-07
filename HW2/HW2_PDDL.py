from unified_planning.shortcuts import *
from unified_planning.model.metrics import *
from unified_planning.io import PDDLWriter
from unified_planning.shortcuts import *
import unified_planning.shortcuts
import time
import warnings
import numpy as np
warnings.filterwarnings("ignore")


def Dys(orb_rad, EforSat, EforLunch):
    # TODO: Declare Types

    EforBuild = 0.02976 # Energy for building one satellite in [10^10 Watt-month]

    Location = UserType("Location") # Earth/Mercury/Orbit

    # TODO: Create Predicates

    # Boolean Fluents
    IsCrewBuilt = Fluent("BuildCrew", BoolType())    # Is there an Autonomous crew for building satellites on mercury? (True/False)
    IsCrewLunched = Fluent("LaunchCrew", BoolType())    # Is crew already lunched? (True/False)
    IsEarthSat = Fluent("IsEarthSat", BoolType())    # Is satellites on earth already built? (True/False)

    # Numeric Fluents
    SatNum = Fluent("SatNum", RealType(), l=Location)  # How many Satellites there is on Earth/Orbit/mercury?
    Distance = Fluent("Distance", RealType(), l_from=Location, l_to=Location)  # How much distance there is between 2 locations in time units?
    Power = Fluent("Power", RealType())  # How much Power is harvested by the satellites at current time?
    CrewStations = Fluent("Crew", RealType()) # Construction team size
    TempSat = Fluent("TempSat", RealType()) # Temporary variable for lunching satellites

    # TODO: Declaring objects

    Mercury = Object("Mercury", Location)
    Earth = Object("Earth", Location)
    Orbit = Object("Orbit", Location)
    objects = [Mercury, Earth, Orbit]

    # TODO: Create Actions with Parameters ,Durative Preconditions and Effects

    #1 Construct initial amount of satellites on earth.
    BuildSatEarth = DurativeAction('BuildSatEarth')
    BuildSatEarth.set_fixed_duration(60) # 5 years for building 100000 satellites
    BuildSatEarth.add_condition(StartTiming(), Not(IsEarthSat)) # Ensure that this action can be executed only once.
    BuildSatEarth.add_effect(StartTiming(), IsEarthSat, True)
    BuildSatEarth.add_effect(EndTiming(), SatNum(Earth), SatNum(Earth) + 100000)

    #2 Construct autonomous workers that will deploy on mercury and will be able to build satellites.
    BuildCrewEarth = DurativeAction('BuildCrewEarth')
    BuildCrewEarth.set_fixed_duration(60) # Fixed duration of the building the autonomous crew.
    BuildCrewEarth.add_condition(StartTiming(), Not(IsCrewBuilt)) # Ensures that action can be taken only once.
    BuildCrewEarth.add_effect(EndTiming(), IsCrewBuilt, True)

    #3 Lunch the satellites from Earth to orbit.
    LunchSatEarth = DurativeAction('LunchSatEarth')
    LunchSatEarth.set_fixed_duration(Distance(Earth, Orbit))
    LunchSatEarth.add_condition(StartTiming(), GT(SatNum(Earth), 0)) # Ensure that there are satellites on earth to lunch.
    LunchSatEarth.add_effect(EndTiming(), SatNum(Orbit), SatNum(Orbit) + SatNum(Earth)) # Add the amount of satellites on earth to the amount of satellites in orbit.
    LunchSatEarth.add_effect(EndTiming(), SatNum(Earth), 0)
    LunchSatEarth.add_effect(EndTiming(), Power, Power + SatNum(Earth) * EforSat) # Power is increased by the amount of energy that is harvested by the satellites.

    #4 Lunch the satellites from Mercury to orbit.
    LunchSatMerc = DurativeAction('LunchSatMerc')
    LunchSatMerc.set_fixed_duration(Distance(Mercury, Orbit))
    LunchSatMerc.add_condition(StartTiming(), GT(SatNum(Mercury), 0)) # Ensure that there are satellites on mercury to lunch.
    LunchSatMerc.add_condition(StartTiming(), GE(Power, EforLunch * Distance(Mercury, Orbit))) # Ensure that there is enough power to lunch the satellites.
    LunchSatMerc.add_effect(StartTiming(), Power, Power - EforLunch * Distance(Mercury, Orbit))
    LunchSatMerc.add_effect(StartTiming(), TempSat, SatNum(Mercury))
    LunchSatMerc.add_effect(StartTiming(), SatNum(Mercury), 0)
    LunchSatMerc.add_effect(EndTiming(), SatNum(Orbit), SatNum(Orbit) + TempSat)
    LunchSatMerc.add_effect(EndTiming(), TempSat, 0)
    LunchSatMerc.add_effect(EndTiming(), Power, Power + EforLunch * Distance(Mercury, Orbit) + SatNum(Mercury) * EforSat) # Power is increased by the amount of energy that is harvested by the satellites.

    #5 Lunch the autonomous crew from Earth to Mercury.
    LunchCrew = DurativeAction('LunchCrew')
    LunchCrew.set_fixed_duration(60)
    LunchCrew.add_condition(StartTiming(), IsCrewBuilt)
    LunchCrew.add_condition(StartTiming(), IsEarthSat)
    LunchCrew.add_condition(StartTiming(), Not(IsCrewLunched))
    LunchCrew.add_effect(EndTiming(), IsCrewLunched, True)

    #6 Build satellites in exponential increase.
    BuildSatMer = DurativeAction('BuildSatMer')
    # l = BuildSatMer.parameter('l')
    BuildSatMer.set_fixed_duration(6) # Fixed duration of 6 months.
    BuildSatMer.add_condition(StartTiming(), GE(Power, CrewStations * 10000 * EforBuild))
    BuildSatMer.add_condition(StartTiming(), IsCrewLunched) # Ensure that there is a construction crew on mercury.
    BuildSatMer.add_effect(StartTiming(), Power, Power - CrewStations * 10000 * EforBuild)
    BuildSatMer.add_effect(EndTiming(), SatNum(Mercury), SatNum(Mercury) + (CrewStations * 10000))
    BuildSatMer.add_effect(EndTiming(), Power, Power + CrewStations * 10000 * EforBuild)

    #7 Expand the satellite building capabilities of the autonomous crew.
    ExpandCrew = DurativeAction('ExpandCrew')
    ExpandCrew.set_fixed_duration(6) # Fixed duration of 0.5 years.
    ExpandCrew.add_condition(StartTiming(), IsCrewLunched)
    ExpandCrew.add_condition(StartTiming(), GE(Power, EforBuild * 2000)) # the condition to expand the crew is at least 1/5 power of the action of building satellites.
    ExpandCrew.add_effect(StartTiming(), Power, Power - EforBuild * 2000)
    ExpandCrew.add_effect(EndTiming(), Power, Power + EforBuild * 2000)
    ExpandCrew.add_effect(EndTiming(), CrewStations, CrewStations + 1)

    # TODO: Load the domain into the problem and add objects

    Dyson_Swarm = Problem("Dyson_Swarm")
    Dyson_Swarm.add_objects(objects)
    Dyson_Swarm.add_fluent(IsCrewBuilt, default_initial_value=False)
    Dyson_Swarm.add_fluent(IsCrewLunched, default_initial_value=False)
    Dyson_Swarm.add_fluent(IsEarthSat, default_initial_value=False)
    Dyson_Swarm.add_fluent(SatNum, default_initial_value=0)
    Dyson_Swarm.add_fluent(Distance, default_initial_value=0)
    Dyson_Swarm.add_fluent(Power, default_initial_value=0)
    Dyson_Swarm.add_fluent(TempSat, default_initial_value=0)
    Dyson_Swarm.add_fluent(CrewStations, default_initial_value=1)
    Dyson_Swarm.add_action(BuildSatEarth)
    Dyson_Swarm.add_action(LunchSatEarth)
    Dyson_Swarm.add_action(LunchSatMerc)
    Dyson_Swarm.add_action(LunchCrew)
    Dyson_Swarm.add_action(BuildSatMer)
    Dyson_Swarm.add_action(ExpandCrew)
    Dyson_Swarm.add_action(BuildCrewEarth)

    # TODO: Declare intitial state

    # Set initial values of boolean fluents
    Dyson_Swarm.set_initial_value(IsCrewBuilt, False)
    Dyson_Swarm.set_initial_value(IsCrewLunched, False)
    Dyson_Swarm.set_initial_value(IsEarthSat, False)


    # Set initial values of numeric fluents
    Dyson_Swarm.set_initial_value(SatNum(Earth), 0)
    Dyson_Swarm.set_initial_value(SatNum(Orbit), 0)
    Dyson_Swarm.set_initial_value(SatNum(Mercury), 0)
    Dyson_Swarm.set_initial_value(Power, 0)

    dist_dict = {'Earth2Mercury': 4.8, 'Earth2Orbit': orb_rad, 'Mercury2Orbit': orb_rad - 4.8}  # Distance between locations in time units.

    Dyson_Swarm.set_initial_value(Distance(Earth, Mercury), dist_dict['Earth2Mercury'])
    Dyson_Swarm.set_initial_value(Distance(Earth, Orbit), dist_dict['Earth2Orbit'])
    Dyson_Swarm.set_initial_value(Distance(Mercury, Orbit), dist_dict['Mercury2Orbit'])


    # TODO: Set the Goals

    Dyson_Swarm.add_goal(GE(SatNum(Orbit), 200000))
    # Dyson_Swarm.add_quality_metric(MinimizeMakespan()) """ Metric to minimize the time for number of satellites in orbit."""

    # TODO: write the PDDL file

    w = PDDLWriter(Dyson_Swarm)
    w.write_domain('domain_Dyson_Swarm.pddl')
    w.write_problem('problem_Dyson_Swarm.pddl')

    # TODO: Solve the problem using the UPF planner

    up.shortcuts.get_env().credits_stream = None
    with OneshotPlanner(name='tamer') as planner:
        result = planner.solve(Dyson_Swarm)
        plan = result.plan
        if plan is not None:
            print("%s returned:" % planner.name)
            for start, action, duration in plan.timed_actions:
                print("%s: %s [%s]" % (float(start), action, float(duration)))
            # print("%s returned:" % planner.name)
            # print(plan)
            print()
            Get_Final_Values(Dyson_Swarm, plan, EforSat)
        else:
            print("No plan found.")
    return

def Get_Final_Values(problem, plan, EforSat):

    """
    This function is used to get the final values of the numeric fluents after the plan is executed.
    EforSat is the energy the 1 satellite on orbit is harvesting. it depeneds on the orbit distance from the sun.

    The function prints the numeric fluents values after each action in the plan in order to follow it.
    """

    Sats_Mer = 0
    Sats_Orb = 0
    crew = 1
    Power = 0
    print('Init Sats_orb: ', Sats_Orb)

    for a in plan.timed_actions:
        if str(a[1]) == 'LunchSatEarth':
            Sats_Orb += 100000
            Power += Sats_Orb * EforSat
            print('LunchSatEarth: ')
            print('| Sats_Mer:', Sats_Mer, '| Sats_Orb:', Sats_Orb, '| crew:', crew, '| Power:', Power)
        elif str(a[1]) == 'ExpandCrew':
            crew += 1
            print('ExpandCrew')
            print('| Sats_Mer:', Sats_Mer, '| Sats_Orb:', Sats_Orb, '| crew:', crew, '| Power:', Power)
        elif str(a[1]) == 'LunchSatMerc':
            Sats_Orb += Sats_Mer
            Sats_Mer = 0
            Power += Sats_Orb * EforSat
            print('LunchSatMerc')
            print('| Sats_Mer:', Sats_Mer, '| Sats_Orb:', Sats_Orb, '| crew:', crew, '| Power:', Power)
        elif str(a[1]) == 'LunchCrew':
            print('LunchCrew')
        elif str(a[1]) == 'BuildCrewEarth':
            print('BuildCrewEarth')
        elif str(a[1]) == 'BuildSatEarth':
            print('BuildSatEarth')
        elif str(a[1]) == 'BuildSatMer':
            Sats_Mer += 10000 * crew
            print('BuildSatMer')
            print('| Sats_Mer:', Sats_Mer, '| Sats_Orb:', Sats_Orb, '| crew:', crew, '| Power:', Power)

    print('Final Sats_orb: ', Sats_Orb)
    print('Final Sats_mer: ', Sats_Mer)
    print('Final Crew: ', crew)
    print('Power: ', Power)
    return

def Orbit2year(orbits):
    m = (15-5.8)/(4*12/10)
    T = (15 - orbits)/m
    return T

if __name__ == '__main__':
    Orbits = np.arange(5, 7, 0.2) # [10^7 m]
    Efficiencies = [0.06, 0.12, 0.18, 0.24, 0.3,  0.36, 0.42, 0.48, 0.48, 0.48] # efficiency of the solar panels per orbit
    EforSatt = [1.46, 2.69, 3.74, 4.64, 5.41, 6.06, 6.63, 7.11, 6.68, 6.29] # Energy harvested per satellite for each orbit [10^10 Watt-month]
    Travel_Time = Orbit2year(Orbits)

    for i in range(len(Orbits)):
        start = time.time()
        Dys(orb_rad=Travel_Time[i], EforSat=EforSatt[i], EforLunch=abs(Orbits[i]))
        end = time.time()
        t = end - start
        print('Time: ', t)