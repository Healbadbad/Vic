# Given a variable

# Keeps track of the history of values
# plots them


# Potentially tracks Deltas

# import matplotlib
# from matplotlib import pyplot as plt
# matplotlib.use('GTKAgg')

def tracker_decorator(function):
    history = []
    history_map = {}
    # Replace with a Queue?
    # print()
    #def wrapper(**kwargs):
    def wrapper(*args):
        print("args:", *args)
        print("locals:", locals())
        print("globals:", globals())
        print("vars:", vars())
        print("inner id: ", id(args[0]))
        # print("kwargs:", kwargs)
        # print(dir(args))
        rv = function(*args)
        history.append(*args)
        print(history)
        return rv

    return wrapper

@tracker_decorator
def track(variable):
    return variable




# def run(niter=1000, doblit=True):
#     """
#     Display the simulation using matplotlib, optionally using blit for speed
#     """

#     fig, ax = plt.subplots(1, 1)
#     ax.set_aspect('equal')
#     ax.set_xlim(0, 255)
#     ax.set_ylim(0, 255)
#     ax.hold(True)
#     rw = randomwalk()
#     x, y = rw.next()

#     plt.show(False)
#     plt.draw()

#     if doblit:
#         # cache the background
#         background = fig.canvas.copy_from_bbox(ax.bbox)

#     points = ax.plot(x, y, 'o')[0]
#     tic = time.time()

#     for ii in xrange(niter):

#         # update the xy data
#         x, y = rw.next()
#         points.set_data(x, y)

#         if doblit:
#             # restore background
#             fig.canvas.restore_region(background)

#             # redraw just the points
#             ax.draw_artist(points)

#             # fill in the axes rectangle
#             fig.canvas.blit(ax.bbox)

#         else:
#             # redraw everything
#             fig.canvas.draw()

#     plt.close(fig)
#     print "Blit = %s, average FPS: %.2f" % (
#         str(doblit), niter / (time.time() - tic))


if __name__ == "__main__":
    import inspect
    for i in range(5):
        track(i)
        print("outer id: ", id(i))
        # j = i + 20
        # track(j)
        frame = inspect.currentframe()
        print(frame)
    