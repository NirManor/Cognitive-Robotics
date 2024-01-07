import math
import matplotlib.pyplot as plt
import numpy as np

def calculate_iterations(total_satellites, s, es, target_surface_percent, distance):

  Tarr = np.array([0])
  SurArr = np.array([0])
  EngTotArray = np.array([0])
  # Calculate the solar constant
  solar_constant = 3.95*10**6 # W/m^2
  i=0
  t=0
  Norm_surface=s*10**(-10)
  # es - The energy required to create a 1 meter panel from energy capture in 1 week (Watt/week)

  es_norm= (es/2)*Norm_surface*10**3
  # time required for the satellite to get to the orbit
  Dist_from_Mer= abs(distance-5.8)
  time_to_lunch= (Dist_from_Mer/5.8)*(78840000/10)+86400

  # Calculate the capture efficiency based on the distance from the sun
  capture_efficiency = 0.3 * (distance - 5.80) + 0.3
  if capture_efficiency>0.48:
    capture_efficiency=0.48

  # Calculate the target surface area
  target_surface = target_surface_percent * (4 * math.pi * distance**2)

  print("sun Iradiance:",solar_constant / (4 * math.pi * distance**2))

  print("capture efficiency:",capture_efficiency)



  # Calculate the total energy captured by all of the satellites in one iteration
  total_energy = total_satellites * Norm_surface * capture_efficiency * solar_constant / (4 * math.pi * distance**2)

  # Calculate the total surface area covered by all of the satellites in one iteration
  total_surface = total_satellites * Norm_surface

  # Check if the target surface has been reached

  while total_surface <= target_surface:



    total_surface = total_satellites * Norm_surface
    total_energy = total_satellites * Norm_surface * capture_efficiency * solar_constant / (4 * math.pi * distance**2)
    EforSat = (total_energy/(total_satellites))*((10**10)/(2*259200))# for KWATT Energy for one satellite in 0.5 year
    # new_satellites = (total_energy-total_energy_temp) / (es_norm)
    # total_satellites = total_satellites + new_satellites
    total_satellites+=total_energy/es_norm
    t+=3600*24*7 + time_to_lunch
    i+=1

    Tarr = np.append(Tarr, [t/(2592000*12)])
    SurArr=np.append(SurArr, [total_surface/target_surface])
    EngTotArray=np.append(EngTotArray, total_energy)

  return i, t, total_energy, Tarr, SurArr, EngTotArray, capture_efficiency, EforSat


# Example usage
Distace_sun=5.8

# Create the figure and axes objects
# plt.figure(figsize=(30, 30))
fig, ax = plt.subplots()
for Distace_sun in np.arange(5, 7, 0.2):
  iterations, time, Total_Energy, TimeArr, SurfaceArr, EnergyArray, Eff, EforSat = calculate_iterations(1000000, 1000, 1190, 0.9, Distace_sun)
  print("num of iterations:{}\n".format(iterations))
  print("time in years:{}\n".format(time / (3600 * 24 * 30 * 12)))
  print("the total energy:{}[10^26-Watt]\n".format(Total_Energy * 10 ** (-6)))
  label1 = str(Distace_sun) + " 10^10[m]"

  ax.plot(TimeArr,SurfaceArr,label='dis: ' + ("%.3f [10^10 [m]]" % Distace_sun)+' | Time: '+("%.2f [Yr]" % (time / (3600 * 24 * 30 * 12)))+" | Eff: "+ ("%.3f" % (Eff)) +" | EforSatt: "+ ("%.2f [10^10 [Watt-month]]" % (EforSat)))

  # ax = plt.axes(projection='3d')
  #
  # ax.plot(TimeArr, SurfaceArr,EnergyArray* 10 ** (-6))
  ax.set_xlabel("Time in years")
  ax.set_ylabel("Covered_Surface")

  # ax.set_zlabel("Total Energy in 10^26")

  # plt.legend([label1])
  # plt.xlabel('Time in years')
  # plt.ylabel('Covered Surface')
  # plt.title("Time to cover 90% as function of distance")
# Add a legend
ax.grid()
ax.legend(loc='lower right', prop={'size': 8})
plt.savefig('HW2_Cal.png')

# Show the plot
plt.show()



# n: The number of satellites at the start of the iteration.
# s: The surface area of each satellite (in m^2).
# e: The base capture efficiency of each satellite (a value between 0 and 1).
# es: The energy required to create a single satellite (in J).
# c: The energy conversion efficiency (a value between 0 and 1).
# target_surface: The target surface area that you want to cover with satellites (in m^2).
# distance: The distance from the sun at which the satellites are placed (in 10^10 m).

# from mpl_toolkits.mplot3d.axes3d import Axes3D
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
#
# datasets = [{"x":[1,2,3], "y":[1,4,9], "z":[0,0,0], "colour": "red"} for _ in range(6)]
#
# for dataset in datasets:
#     ax.plot(dataset["x"], dataset["y"], dataset["z"], color=dataset["colour"])
#
# plt.show()