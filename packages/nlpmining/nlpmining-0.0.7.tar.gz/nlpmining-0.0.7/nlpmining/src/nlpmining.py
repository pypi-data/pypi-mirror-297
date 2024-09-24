class printer:
    def __init__(self):
        self.a = 1

    def DSP_symmetirc_testing(selfs):
        print('''
        encrypt.py
        import subprocess
        # OpenSSL command to encrypt the file
        
        # openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 1000 -salt -in message.txt -out encrypt.enc
        command = [
            "openssl", "enc", "-aes-256-cbc", "-md", "sha512", "-pbkdf2", "-iter", "1000", "-salt",
            "-in", "message.txt", "-out", "encrypt_1.enc"
        ]
        
        try:
            # Run the OpenSSL command
            subprocess.run(command, check=True)
            print("File encrypted and saved to 'encrypt.enc'.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during encryption: {e}")
        
        decrypt.py
        import subprocess
        # OpenSSL command to decrypt the file
        
        # openssl enc -aes-256-cbc -md sha512 -pbkdf2 -iter 1000 -salt -in encrypt.enc -out decrypt.txt -d
        command = [
            "openssl", "enc", "-aes-256-cbc", "-md", "sha512", "-pbkdf2", "-iter", "1000", "-d",
            "-in", "encrypt_1.enc", "-out", "decrypt_1.txt"
        ]
        
        try:
            # Run the OpenSSL command
            subprocess.run(command, check=True)
            print("File decrypted and saved to 'decrypt.txt'.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during decryption: {e}")

        ''')

    def DSP_signatures(self):
        print('''
        sign.py
        import subprocess
        # Step 1: Generate a digital signature using the private key
        command = [
            "openssl", "dgst", "-sha256", "-sign", "myprivate.key", "-out", "signature.bin", "message.txt"
        ]
        
        try:
            # Run the OpenSSL command to generate the signature
            subprocess.run(command, check=True)
            print("Digital signature generated and saved as 'signature.bin'.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during signature generation: {e}")
        
        verify.py
        import subprocess
        # Step 2: Verify the digital signature using the public key
        command = [
            "openssl", "dgst", "-sha256", "-verify", "mypublic.key", "-signature", "signature.bin", "message.txt"
        ]
        
        try:
            # Run the OpenSSL command to verify the signature
            subprocess.run(command, check=True)
            print("Signature verification successful.")
        except subprocess.CalledProcessError as e:
            print(f"Signature verification failed: {e}")

        ''')

    def DSP_RSA(self):
        print('''
        encrypt.py
        import subprocess

        # OpenSSL command to encrypt using the public key
        # openssl pkeyutl -encrypt -in message.txt -pubin -inkey mypublic.key -out encrypt.enc
        command = [
            "openssl", "pkeyutl", "-encrypt", "-in", "message.txt", "-pubin", "-inkey", "mypublic.key", "-out", "encrypt.enc"
        ]
        
        try:
            # Run the OpenSSL command to encrypt the file
            subprocess.run(command, check=True)
            print("File encrypted and saved to 'encrypt.enc'.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during encryption: {e}")
        
        decrypt.py
        import subprocess
        
        # OpenSSL command to decrypt using the private key
        # openssl pkeyutl -decrypt -in encrypt.enc -inkey myprivate.key -out decrypt.txt
        command = [
            "openssl", "pkeyutl", "-decrypt", "-in", "encrypt.enc", "-inkey", "myprivate.key", "-out", "decrypt.txt"
        ]
        
        try:
            # Run the OpenSSL command to decrypt the file
            subprocess.run(command, check=True)
            print("File decrypted and saved to 'decrypt.txt'.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during decryption: {e}")
        
        generate keys.py
        import subprocess
        # Command to generate a private key with AES-256-CBC encryption
        # openssl genrsa -aes-256-cbc -out myprivate.key
        generate_private_key = [
            "openssl", "genrsa", "-aes-256-cbc", "-out", "myprivate.key"
        ]
        
        # Command to generate a public key from the private key
        # openssl rsa -in myprivate.key -pubout > mypublic.keys
        generate_public_key = [
            "openssl", "rsa", "-in", "myprivate.key", "-pubout", "-out", "mypublic.key"
        ]
        
        try:
            # Run the command to generate the private key
            subprocess.run(generate_private_key, check=True)
            print("Private key saved as 'myprivate.key'.")
            
            # Run the command to generate the public key
            subprocess.run(generate_public_key, check=True)
            print("Public key saved as 'mypublic.key'.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during key generation: {e}")

        ''')

    def NS_critical_threshold(self):
        print('''
        import numpy as np
        from scipy.special import erf
        from scipy.integrate import quad

        # Function to calculate <k> and <k^2> for a power law with exponential cutoff
        def power_law_exponential_cutoff(gamma, k_c, k_min=1, k_max=np.inf):
            k_avg = quad(lambda k: k * (k**(-gamma) * np.exp(-k/k_c)), k_min, k_max)[0]
            k2_avg = quad(lambda k: k**2 * (k**(-gamma) * np.exp(-k/k_c)), k_min, k_max)[0]
            return k_avg, k2_avg

        # Function to calculate <k> and <k^2> for a lognormal distribution
        def lognormal_distribution(mu, sigma, k_min=1, k_max=np.inf):
            k_avg = quad(lambda k: k * (1/(k * sigma * np.sqrt(2 * np.pi)) * np.exp(- (np.log(k) - mu)**2 / (2 * sigma**2))), k_min, k_max)[0]
            k2_avg = quad(lambda k: k**2 * (1/(k * sigma * np.sqrt(2 * np.pi)) * np.exp(- (np.log(k) - mu)**2 / (2 * sigma**2))), k_min, k_max)[0]
            return k_avg, k2_avg

        # Function to calculate <k> and <k^2> for a delta distribution (all nodes have the same degree)
        def delta_distribution(k0):
            k_avg = k0
            k2_avg = k0**2
            return k_avg, k2_avg

        # Function to calculate the critical threshold f_c
        def critical_threshold(k_avg, k2_avg):
            return 1 - (k_avg / k2_avg)

        # Example usage
        gamma = 2.5  # Example value for power law
        k_c = 100     # Example cutoff
        mu = 2       # Mean for lognormal
        sigma = 0.5  # Standard deviation for lognormal
        k0 = 10       # Degree for delta distribution

        # Calculate <k> and <k^2> for each distribution
        k_avg_power, k2_avg_power = power_law_exponential_cutoff(gamma, k_c)
        k_avg_lognormal, k2_avg_lognormal = lognormal_distribution(mu, sigma)
        k_avg_delta, k2_avg_delta = delta_distribution(k0)

        # Calculate the critical threshold for each distribution
        fc_power = critical_threshold(k_avg_power, k2_avg_power)
        fc_lognormal = critical_threshold(k_avg_lognormal, k2_avg_lognormal)
        fc_delta = critical_threshold(k_avg_delta, k2_avg_delta)

        print(f"Critical threshold for power law with exponential cutoff: {fc_power}")
        print(f"Critical threshold for lognormal distribution: {fc_lognormal}")
        print(f"Critical threshold for delta distribution: {fc_delta}")

        ''')

    def NS_avalanche(self):
        print('''
        import networkx as nx
        import random
        import numpy as np
        import matplotlib.pyplot as plt

        # Parameters
        N = 10  # Number of nodes
        average_degree = 2  # Average degree

        # Function to generate an Erdős-Rényi network
        def generate_erdos_renyi(N, average_degree):
            p = average_degree / (N - 1)  # Probability for Erdős-Rényi model
            G = nx.erdos_renyi_graph(N, p)
            return G

        # Function to generate a scale-free network using Barabási-Albert model
        def generate_scale_free(N, average_degree):
            m = average_degree // 2  # Parameter for the number of edges to attach per new node
            G = nx.barabasi_albert_graph(N, m)
            return G

        # Initialize buckets (number of grains in each node)
        def initialize_buckets(G):
            return {node: 0 for node in G.nodes()}

        # Get the bucket capacity (equal to node degree)
        def get_bucket_capacity(G):
            return {node: G.degree[node] for node in G.nodes()}

        # Simulate adding a grain and handling toppling (avalanche)
        def simulate_avalanche(G, buckets, capacities):
            avalanche_sizes = []

            def topple(node):
                # Start an avalanche from the given node
                toppled_nodes = set()
                to_process = [node]

                while to_process:
                    current_node = to_process.pop()
                    if buckets[current_node] >= capacities[current_node]:
                        toppled_nodes.add(current_node)
                        # Topple: Redistribute grains to neighbors
                        grains_to_redistribute = buckets[current_node]
                        buckets[current_node] = 0  # Reset bucket after toppling

                        for neighbor in G.neighbors(current_node):
                            buckets[neighbor] += 1
                            # If neighbor becomes unstable, it will topple
                            if buckets[neighbor] >= capacities[neighbor]:
                                to_process.append(neighbor)

                return len(toppled_nodes)  # Avalanche size

            # Randomly choose a node to add a grain
            random_node = random.choice(list(G.nodes()))
            buckets[random_node] += 1

            # Check if it needs to topple
            if buckets[random_node] >= capacities[random_node]:
                avalanche_size = topple(random_node)
                avalanche_sizes.append(avalanche_size)
            else:
                avalanche_sizes.append(0)

            return avalanche_sizes

        # Simulation function
        def run_simulation(G, steps):
            # Initialize the buckets and capacities
            buckets = initialize_buckets(G)
            capacities = get_bucket_capacity(G)

            # Simulate avalanches for a number of steps
            avalanche_sizes = []
            for _ in range(steps):
                avalanche_sizes.extend(simulate_avalanche(G, buckets, capacities))

            return avalanche_sizes

        # Generate networks
        G_erdos_renyi = generate_erdos_renyi(N, average_degree)
        G_scale_free = generate_scale_free(N, average_degree)

        # Run simulations
        steps = 1000  # Number of time steps

        # Erdős-Rényi simulation
        avalanche_sizes_erdos = run_simulation(G_erdos_renyi, steps)

        # Scale-Free simulation
        avalanche_sizes_scale_free = run_simulation(G_scale_free, steps)

        # Display results
        print("Avalanche sizes (Erdős-Rényi):", avalanche_sizes_erdos)
        print("Avalanche sizes (Scale-Free):", avalanche_sizes_scale_free)

        # Plot the networks
        plt.figure(figsize=(10, 5))

        plt.subplot(121)
        nx.draw(G_erdos_renyi, with_labels=True, node_color='skyblue', node_size=500, edge_color='gray')
        plt.title("Erdős-Rényi Network")

        plt.subplot(122)
        nx.draw(G_scale_free, with_labels=True, node_color='lightgreen', node_size=500, edge_color='gray')
        plt.title("Scale-Free Network")

        plt.show()
        ''')

    def IR_rocchio(self):
        print('''
        import numpy as np
        from sklearn.feature_extraction.text import TfidfVectorizer

        # Example documents and query
        documents = [
            "the cat in the hat",
            "the quick brown fox",
            "the cat and the hat",
            "the quick red fox",
            "the fox and the cat"
        ]

        query = "cat fox"

        # Relevance feedback
        relevant_docs_indices = [0, 2]  # indices of relevant documents
        non_relevant_docs_indices = [1, 3]  # indices of non-relevant documents

        # Parameters for Rocchio algorithm
        alpha = 1.0
        beta = 0.75
        gamma = 0.15

        # Preprocessing: TF-IDF vectorization
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(documents)
        query_vector = vectorizer.transform([query])

        # Rocchio Algorithm
        def rocchio(query_vector, tfidf_matrix, relevant_indices, non_relevant_indices, alpha, beta, gamma):
            # Compute the centroids of relevant and non-relevant documents
            relevant_docs = tfidf_matrix[relevant_indices]
            non_relevant_docs = tfidf_matrix[non_relevant_indices]

            # Average relevant and non-relevant document vectors
            if len(relevant_indices) > 0:
                relevant_centroid = relevant_docs.mean(axis=0)
            else:
                relevant_centroid = np.zeros(query_vector.shape)

            if len(non_relevant_indices) > 0:
                non_relevant_centroid = non_relevant_docs.mean(axis=0)
            else:
                non_relevant_centroid = np.zeros(query_vector.shape)

            # Rocchio update formula
            new_query_vector = alpha * query_vector + beta * relevant_centroid - gamma * non_relevant_centroid

            return new_query_vector

        # Compute the new query vector using Rocchio algorithm
        new_query_vector = rocchio(query_vector, tfidf_matrix, relevant_docs_indices, non_relevant_docs_indices, alpha, beta, gamma)

        # Print the updated query vector
        print("Updated Query Vector (TF-IDF values):")
        print(new_query_vector)

        # Ranking documents based on new query vector
        def rank_documents(new_query_vector, tfidf_matrix):
            # Compute cosine similarity between new query vector and document vectors
            scores = (tfidf_matrix * new_query_vector.T).toarray().flatten()

            # Rank documents based on scores
            ranked_docs = np.argsort(scores)[::-1]

            for i, doc_index in enumerate(ranked_docs):
                print(f"Rank {i+1}: Document {doc_index+1} (Score: {scores[doc_index]:.4f}) - '{documents[doc_index]}'")

        # Rank documents using the updated query vector
        rank_documents(new_query_vector, tfidf_matrix)
        ''')

    def IR_BIM(self):
        print('''
        import numpy as np
        import pandas as pd

        # Example documents and query
        documents = [
            "the cat in the hat",
            "the quick brown fox",
            "the cat and the hat",
            "the quick red fox",
            "the fox and the cat"
        ]

        query = "cat fox"

        # Preprocessing: Tokenize documents and query
        def tokenize(doc):
            return doc.lower().split()

        doc_tokens = [set(tokenize(doc)) for doc in documents]
        query_tokens = set(tokenize(query))

        # Inverse document frequency calculation
        def compute_idf(doc_tokens, num_docs):
            term_doc_count = {}
            for tokens in doc_tokens:
                for token in tokens:
                    if token in term_doc_count:
                        term_doc_count[token] += 1
                    else:
                        term_doc_count[token] = 1

            idf = {}
            for term, count in term_doc_count.items():
                idf[term] = np.log((num_docs - count + 0.5) / (count + 0.5))

            return idf

        # Binary Independence Model
        def compute_bim_score(doc_tokens, query_tokens, idf, num_docs):
            scores = []

            for tokens in doc_tokens:
                score = 0
                for term in query_tokens:
                    if term in idf:
                        if term in tokens:  # Term is present in document
                            score += idf[term]
                        else:  # Term is not present in document
                            score += np.log((0.5) / (num_docs + 0.5))
                scores.append(score)

            return scores

        # Main function to compute and rank documents
        def rank_documents(documents, query):
            num_docs = len(documents)
            idf = compute_idf(doc_tokens, num_docs)
            scores = compute_bim_score(doc_tokens, query_tokens, idf, num_docs)

            ranked_docs = np.argsort(scores)[::-1]

            for i, doc_index in enumerate(ranked_docs):
                print(f"Rank {i+1}: Document {doc_index+1} (Score: {scores[doc_index]:.4f}) - '{documents[doc_index]}'")

        # Rank documents based on query
        rank_documents(documents, query)
        ''')

        return None
