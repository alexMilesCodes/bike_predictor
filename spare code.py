alts = np.zeros(max(ref_x)-min(ref_x)+1)
    for i in range(len(ref_x)-1):
        alts[ref_x[i] - min(ref_x)] = ref_alt.get(ref_x[i])
        for p in range(ref_x[i]+1, int(math.ceil((ref_x[i] + ref_x[i+1])/2))):
            alt = -1
            rol = [gs[top, p], gs[top+1, p], gs[top+2, p]]
            av = sum(rol)/len(rol)
            h = top+2
            while alt == -1 and h < bot:
                old_av = av
                h += 1
                rol = rol[1:]+gs[h, p]
                av = np.mean(rol)
            if av < old_av - 5:
                i = i
                while alts[p-min(ref_x)-i] == -1:
                    i += 1
                if abs(h-alts[p-min(ref_x)+i]) < 15:
                    alt = h-2
            alts[p - min(ref_x)] = alt
        alts[ref_x[i+1]-min(ref_x)] = ref_alt.get(ref_x[i+1])
        for p in (np.arange(ref_x[i+1]-1, int(math.ceil((ref_x[i] + ref_x[i+1])/2)), -1)-1).astype(int):
            alt = -1
            rol = [gs[top, p], gs[top + 1, p], gs[top + 2, p]]
            av = sum(rol)/len(rol)
            h = top + 2
            while alt == -1 and h < bot:
                old_av = av
                h += 1
                rol = rol[1:] + gs[h, p]
                av = np.mean(rol)
            if av < old_av - 5:
                i = 1
                while alts[p-min(ref_x)+i] == -1:
                    i += 1
                if abs(h-alts[p-min(ref_x)+i]) < 15:
                    alt = h-2
            alts[p - min(ref_x)] = alt
    # replace missing altitudes
    for i in (np.arange(len(alts)-2)+1).astype(int):
        if alts[i] < 0:
            alts[i] = (alts[i-1]+alts[i+1])/2

multi = 0.5
# sorting out starting end
grad = (y[1] - y[0]) / (x[1] - x[0])
std = np.std(y)
if abs(grad * x[0]) > std * multi:
    x = [-4 * inc, x[0] - std * multi / grad] + x
    y = [(y[0] - std * multi) * np.sign(grad), (y[0] - std * multi) * np.sign(grad)] + y
else:
    y = [y[0] - grad * (x[0] + 4 * inc)] + y
    x = [-4 * inc] + x

# sorting out finishing end
grad = (y[len(x) - 1] - y[len(x) - 2]) / (x[len(x) - 1] - x[len(x) - 2])
std = np.std(y)
print(x[len(x) - 1])
if abs(grad * (profiles['Distance'][i] - x[len(x) - 1])) > std * multi:
    x = x + [x[len(x) - 1] + std * multi / grad, profiles['Distance'][i] + 4 * inc]
    y = y + [(y[len(y) - 1] + std * multi) * np.sign(grad), (y[len(y) - 1] + std * multi) * np.sign(grad)]
else:
    y = y + [y[len(y) - 1] + grad * (profiles['Distance'][i] - x[len(x) - 1] + 4 * inc)]
    x = x + [profiles['Distance'][i] + 4 * inc]



new_x = []
new_y = []
j = 0
while j < len(y) - 1:
    temp_x = [x[j]]
    while y[j] == y[j + 1] and j < len(y) - 2:
        j += 1
        temp_x.append(x[j])
    new_x.append(np.mean(temp_x))
    new_y.append(y[j])
    j += 1
new_x.append(x[j])
new_y.append(y[j])


tck = interpolate.splrep(x, y, s=0)
    x_new = np.arange(0, profiles['Distance'][i], 0.001)
    y_new = interpolate.splev(x_new, tck, der=0)
    plt.plot(x_new, y_new)
    plt.title('Cubic-spline interpolation')
    plt.show()

    # xvals = np.linspace(0, 2*np.pi, 50)
    # yinterp = np.interp(xvals, x, y)







# reset indices first to 'Race'
# data = pd.concat([profiles, races], axis=1).reset_index()





