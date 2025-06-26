import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.use('macosx')
from utils.upper_connections import UPPER_CONNECTIONS
#print(UPPER_CONNECTIONS)
# Given points

#points = np.array([[0.1711534634232521, 0.018619969487190247, 0.01887747272849083], [-0.1711534634232521, -0.018619969487190247, -0.01887747272849083], [0.3544739559292793, 0.0651126354932785, -0.10750758275389671], [-0.37616016715765, -0.027257606387138367, -0.19198418781161308], [0.33087653666734695, -0.03528328239917755, -0.2757328860461712], [-0.1974024698138237, -0.04639716446399689, -0.321645300835371], [0.33087653666734695, -0.03528328239917755, -0.2757328860461712], [0.36580710485577583, -0.01960744336247444, -0.2838260307908058], [0.39578605256974697, -0.007544562220573425, -0.2924291044473648], [0.42363758757710457, 0.00465596467256546, -0.3139225048944354], [0.4479648806154728, 0.008066941052675247, -0.3289734637364745], [0.4260943401604891, -0.04414176568388939, -0.30804236605763435], [0.4510571211576462, -0.04444109741598368, -0.3205623183166608], [0.4640444442629814, -0.037984978407621384, -0.33221572637557983], [0.4692748971283436, -0.02352249249815941, -0.3598354905843735], [0.4153400347568095, -0.05753718363121152, -0.3168379911221564], [0.4477834440767765, -0.06858047284185886, -0.33693193458020687], [0.4550058916211128, -0.061997967306524515, -0.3617551624774933], [0.46292196959257126, -0.04086940735578537, -0.38198041170835495], [0.40189688839018345, -0.06348827295005322, -0.33201640471816063], [0.42538098990917206, -0.07684971019625664, -0.3502478003501892], [0.4361570328474045, -0.06642183661460876, -0.37511102110147476], [0.44486330822110176, -0.04671300761401653, -0.39399393647909164], [0.37800682336091995, -0.06818280555307865, -0.3414825592190027], [0.3924892321228981, -0.08041932247579098, -0.3557058349251747], [0.4047705880366266, -0.07730288617312908, -0.37690791487693787], [0.41085038951132447, -0.06323938351124525, -0.3961627632379532], [-0.1974024698138237, -0.04639716446399689, -0.321645300835371], [-0.22684453334659338, -0.055971354246139526, -0.35208338871598244], [-0.2515403665602207, -0.06353050097823143, -0.37041832134127617], [-0.27117351070046425, -0.0694744773209095, -0.40153405582532287], [-0.29042962938547134, -0.08361230883747339, -0.4226331543177366], [-0.24068939127027988, -0.09685894381254911, -0.4061595167440828], [-0.24866771325469017, -0.11917785927653313, -0.4228584095835686], [-0.25659720599651337, -0.12613307312130928, -0.4369813483208418], [-0.26902906596660614, -0.11669573374092579, -0.4713785834610462], [-0.21726589370518923, -0.101142143830657, -0.4043338829651475], [-0.21828863536939025, -0.12863586097955704, -0.42670253850519657], [-0.22815779969096184, -0.13045527413487434, -0.4595348685979843], [-0.24149850755929947, -0.11709390766918659, -0.48839081451296806], [-0.1952067483216524, -0.09921868378296494, -0.4040980936260894], [-0.19375476241111755, -0.1181030236184597, -0.4263889044523239], [-0.20043788477778435, -0.11862066574394703, -0.4562227241694927], [-0.20762144215404987, -0.11100704595446587, -0.4771124981343746], [-0.18311505764722824, -0.08486408088356256, -0.40230751084163785], [-0.17209572717547417, -0.0969191025942564, -0.4149338873103261], [-0.16670332103967667, -0.09840508364140987, -0.43555968813598156], [-0.16766662150621414, -0.09190700948238373, -0.45921700820326805]])

# Specify the connections between points (indices)
connections = UPPER_CONNECTIONS

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the points

#ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='red')
# Plot the connections
def plot_connections(points):
    ax.clear()
    for i, connection in enumerate(connections):
        #print(i, connection)
        if connection in ((0, 1), (0,2), (1, 3), (2, 4), (3, 5), (5, 27), (4, 6)):
            color = "green"
            dot_color = "red"
        else:
            color = "blue"
            dot_color = "black"
        ax.plot([points[connection[0], 0], points[connection[1], 0]],
                [points[connection[0], 2], points[connection[1], 2]],
                [-points[connection[0], 1], -points[connection[1], 1]], color=color)
        # Plot dots at the connection points
        ax.scatter(points[connection[0], 0], points[connection[0], 2], -points[connection[0], 1], color=dot_color)
        ax.scatter(points[connection[1], 0], points[connection[1], 2], -points[connection[1], 1], color=dot_color)

    # Set labels for the axes
    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    ax.set_zlabel('Y')

    #set range
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(-0.5, 0.1)
    ax.set_zlim(-0.5, 0.1)
    # Show the plot

    #plt.show()
    plt.show(block=False)
    plt.pause(0.001)

    #plt.clf()
    #plt.close()
'''
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mediapipe.python.solutions.upper_connections import UPPER_CONNECTIONS

# Create line and scatter objects
lines = [plt.plot([], [], [], color='blue')[0] for _ in UPPER_CONNECTIONS]
#dots = [plt.scatter([], [], [], color='black')[0] for _ in UPPER_CONNECTIONS]
dots = [plt.scatter([], [], [], color='black') for _ in UPPER_CONNECTIONS]

# Specify the connections between points (indices)
connections = UPPER_CONNECTIONS

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set labels for the axes
ax.set_xlabel('X')
ax.set_ylabel('Z')
ax.set_zlabel('Y')

# Set range
ax.set_xlim(-0.5, 0.5)
ax.set_ylim(-0.5, 0.1)
ax.set_zlim(-0.5, 0.1)


def plot_connections(points):
    for i, connection in enumerate(connections):
        color = "green" if connection in ((0, 1), (0,2), (1, 3), (2, 4), (3, 5), (5, 27), (4, 6)) else "blue"

        lines[i].set_xdata([points[connection[0], 0], points[connection[1], 0]])
        lines[i].set_ydata([points[connection[0], 2], points[connection[1], 2]])
        lines[i].set_zdata([-points[connection[0], 1], -points[connection[1], 1]])

        dots[connection[0]].set_offsets([[points[connection[0], 0], points[connection[0], 2]]])
        dots[connection[1]].set_offsets([[points[connection[1], 0], points[connection[1], 2]]])

    plt.show(block=False)
    plt.pause(0.001)'''

