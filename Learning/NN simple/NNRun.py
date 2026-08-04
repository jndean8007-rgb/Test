import Neural_Net
from sklearn.datasets import fetch_california_housing


def main():
    housing = fetch_california_housing(as_frame=True)
    X = housing.data
    y = housing.target

    print(X.head())
    print(y.head())

    net1 = Neural_Net.Neuralnet(X, y, (3,3), (10,10,2), "Quant")
    print("Untrained prediction:", net1.predict(X.iloc[0]))


if __name__ == '__main__':
    main()