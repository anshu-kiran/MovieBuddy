from graph import create_graph

def main():
    movie_graph = create_graph()

    print("Welcome to the Movie Recommendation Assistant!")
    print("Type 'exit' to end the conversation.\n")

    while True:
        movie_title = input("Enter a movie title (or 'exit' to quit): ")
        if movie_title.lower() == "exit":
            print("Goodbye!")
            break

        genre_preference = input("Enter your preferred genre: ")

        result = movie_graph.invoke({"input": movie_title, "preferences": {"genre": genre_preference}})

        print("\n--- Recommendation ---")
        print(result["output"])
        print("\n")

if __name__ == "__main__":
    main()
