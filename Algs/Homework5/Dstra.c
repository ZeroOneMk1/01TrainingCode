#include <stdio.h>
#include <limits.h>

#define V 10

int minDistance(int dist[], int sptSet[])
{
    int min = INT_MAX, min_index;

    for (int v = 0; v < V; v++)
    {
        if (sptSet[v] == 0 && dist[v] <= min)
        {
            min = dist[v];
            min_index = v;
        }
    }

    return min_index;
}

void printSolution(int dist[], int parent[], int dest)
{
    printf("Shortest Path Length: %d\n", dist[dest]);

    printf("Shortest Path Sequence: ");
    int current = dest;
    while (current != -1)
    {
        switch (current)
        {
        case 0:
            printf("A ");
            break;
        case 1:
            printf("J ");
            break;
        case 2:
            printf("M ");
            break;
        case 3:
            printf("R ");
            break;
        case 4:
            printf("K ");
            break;
        case 5:
            printf("S ");
            break;
        case 6:
            printf("I ");
            break;
        case 7:
            printf("N ");
            break;
        case 8:
            printf("T ");
            break;
        case 9:
            printf("D ");
            break;

        default:
            break;
        }
        current = parent[current];
    }
    printf("\n");
    printf("I was annnoyed at your pick of letters until I saw the path from 0 to 9. Well played.\n");
}

void dstra(int graph[V][V], int src, int dest)
{
    int dist[V];
    int sptSet[V];
    int parent[V];

    for (int i = 0; i < V; i++)
    {
        dist[i] = INT_MAX;
        sptSet[i] = 0;
        parent[i] = -1;
    }

    dist[src] = 0;

    for (int count = 0; count < V - 1; count++)
    {
        int u = minDistance(dist, sptSet);

        sptSet[u] = 1;

        for (int v = 0; v < V; v++)
        {
            if (!sptSet[v] && graph[u][v] && dist[u] != INT_MAX &&
                dist[u] + graph[u][v] < dist[v])
            {
                dist[v] = dist[u] + graph[u][v];
                parent[v] = u;
            }
        }
    }

    printSolution(dist, parent, dest);
}

int main()
{
    int matrix[V][V] = {{0, 54, 11, 13, 0, 0, 0, 0, 0, 0},
                        {54, 0, 37, 0, 3, 0, 102, 0, 0, 0},
                        {11, 37, 0, 10, 36, 19, 0, 0, 0, 0},
                        {13, 0, 10, 0, 0, 18, 0, 0, 7, 0},
                        {0, 3, 36, 0, 0, 15, 124, 123, 0, 0},
                        {0, 0, 19, 18, 15, 0, 0, 138, 8, 0},
                        {0, 102, 0, 0, 124, 0, 0, 9, 0, 72},
                        {0, 0, 0, 0, 123, 138, 9, 0, 146, 67},
                        {0, 0, 0, 7, 0, 8, 0, 146, 0, 213},
                        {0, 0, 0, 0, 0, 0, 72, 67, 213, 0}};

    int start, dest;

    printf("Enter the start node (A=0, J=1, M=2, R=3, K=4, S=5, I=6, N=7, T=8, D=9): ");
    scanf("%d", &start);
    printf("Enter the destination node (A=0, J=1, M=2, R=3, K=4, S=5, I=6, N=7, T=8, D=9): ");
    scanf("%d", &dest);

    dstra(matrix, start, dest);

    return 0;
}
