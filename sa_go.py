from sa import sa
import visualize_tsp

if __name__ == "__main__":
    sa1 = sa()
    sa1.ann()
    sol, pla = sa1.r_sol()
    visualize_tsp.plotTSP([sol], pla)

