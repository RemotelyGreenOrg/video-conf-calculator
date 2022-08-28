# video-conf-calculator
A python-based CO2 calculator for video conferencing.

A live online version is coming soon...

## Installation
*__TODO: Flesh this out__*
```
git clone https://github.com/benkrikler/video-conf-calculator.git
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
# If necessary, build docker image
DOCKER_BUILDKIT=1 docker build -t video-conf-calculator:latest .
```
**Note**: that this should only be temporary before we switch things to be a proper python package, available on PyPI etc.

## Basic usage
*__TODO: Flesh this out__*
```
python -m vc_calculator --help
# Or, on docker
docker run video-conf-calculator:latest --help
```

## How it works
The following description is largely based on [this 2014 paper by Ong et al][1], although we plan to develop this into a more complete and robust model.

The problem of estimating CO2 emissions due to video conferencing can typically be split into two components: the user or client side and the provider or server and infrastructure side.
For each of these, there is an associated lifetime cost due to the hardware components involved, as well as the instantaneous cost due to power consumption.

### Power consumed by a user
To estimate the amount of power consumed, the current model considers the power used by every device that a user might employ to join a video conference.
There are two sources of power consumption for each device:
* The power consumed due to a video conference call is the total power to run
  the device multiplied by the fraction of that power that is used for video
  conferencing.
* The embodied power represents the amount of power used to manufacture and
  deliver the device to the user. This is then multiplied by the fraction of
  the total lifetime of the product that the video conference represents.

The total power of the user's devices is obtained by the sum of the above two terms.

### Power consumed by video servers and network infrastructure
As for the user's direct consumption, the server and network infrastructure also has two sides to power consumption: direct and embodied power.
Network infrastructure is extremely complex with many components playing a role, and not always in a deterministic way.

In the current model, this calculation is simplified by assuming a uniform
power consumption per video call, based on the total bandwidth and power
consumption of "the internet" (based on figures from around 2011).
Thus these two terms of direct and embodied power are given by the
corresponding total power of the entire internet, multiplied by the fraction of
the entire internet's bandwidth that a single video call requires.

### Converting power to CO2 emissions
The total power required for a single user to join a video call is the sum of all terms described above.
In the current model, to convert this power consumption to CO2 emissions, a
simple linear relation is employed where the amount of CO2 produced is assumed
to be directly proportional to the amount of energy consumed.

### Improving this model
There are many ways this model can be improved:
* Develop a more elaborate estimate for the server infrastructure, possibly
  using the links [here][2] and [here][3] (and possibly also [here][4],
  [here][5], and [here][6]).
* Given that power production in different regions can have different
  associated CO2 emissions, the emissions for both the user and infrastructure
  should take this into account rather than the simple linear relation between
  power and emissions that is currently assumed.
* The interface to this model could allow video conferencing providers to directly supply their power consumption for a specific event

## Contributing
*__TODO: Flesh this out__*

## References
- [Ong et al., 2014 - "Comparison of the energy, carbon and time costs..."][1]
- [Foll Thesis, 2008 (French) - "TIC et Énergétique : Techniques d’estimation..."][2]
- [Baliga et al. 2009 - "Carbon footprint of the Internet"][3]
- [Souchon et al. 2007 - "Infrastructure of the information society and its energy demand"][4]
- [Hilty et al. 2015 (German) - "Grüne Software - Schlussbericht zum Vorhaben: Ermittlung..."][5]
- [Hilty et al. 2014 (English) - "The Energy Demand of ICT: A Historical Perspective and..."][6]

[1]: http://www2.eet.unsw.edu.au/~vijay/pubs/jrnl/14comcomVC.pdf 
[2]: http://www.biblioite.ethz.ch/downloads/Souchon_these_version-publique.pdf
[3]: http://dx.doi.org/10.2104/tja09005
[4]: https://ethz.ch/content/dam/ethz/special-interest/mtec/cepe/cepe-dam/documents/people/baebischer/Souchon_6_233.pdf
[5]: http://dx.doi.org/10.13140/2.1.5158.4329
[6]: https://ethz.ch/content/dam/ethz/special-interest/mtec/cepe/cepe-dam/documents/people/baebischer/Aebischer_Hilty_2014_Energy_Demand_ICT_History_Challenges_AAM.pdf
