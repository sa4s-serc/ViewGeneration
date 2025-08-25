import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import shutil

from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from PIL import UnidentifiedImageError
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model


# ---------- Step 1: Feature Extraction ----------
def load_model():
    base_model = VGG16(weights="imagenet")
    return Model(inputs=base_model.input, outputs=base_model.get_layer("fc1").output)



def get_features(img_path, model):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img = img.convert("RGB")  # ensure consistent mode
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x, verbose=0)
        return features.flatten()
    except UnidentifiedImageError:
        print(f"⚠️ Skipping unreadable image: {img_path}")
        return None
    except Exception as e:
        print(f"⚠️ Error processing {img_path}: {e}")
        return None


def extract_features(folder, model):
    features, filenames = [], []
    for fname in os.listdir(folder):
        if fname.lower().endswith((".jpg", ".png", ".jpeg")):
            path = os.path.join(folder, fname)
            feat = get_features(path, model)
            if feat is not None:
                features.append(feat)
                filenames.append(fname)

    features = np.array(features)

    # Scale + sanitize features
    features = StandardScaler().fit_transform(features)
    features = np.nan_to_num(features, nan=0.0, posinf=1e5, neginf=-1e5)
    return features, filenames



# ---------- Step 2: Elbow Plot ----------
def elbow_method(features, max_k=30):
    inertias = []
    for k in range(2, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(features)
        inertias.append(kmeans.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(range(2, max_k + 1), inertias, "bo-")
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("Inertia (Within-Cluster SSE)")
    plt.title("Elbow Method for Optimal k")
    plt.savefig("elbow_method.png", dpi=300, bbox_inches="tight")
    plt.show()


# ---------- Step 3: Clustering ----------
def cluster_features(features, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(features)
    return labels


# ---------- Step 4: Visualization with t-SNE ----------
def visualize_tsne(features, labels):
    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    reduced = tsne.fit_transform(features)

    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(reduced[:, 0], reduced[:, 1], c=labels, cmap="tab10")
    plt.legend(*scatter.legend_elements(), title="Clusters")
    plt.title("Image Clusters (t-SNE)")
    plt.savefig("tsne_visualization.png", dpi=300, bbox_inches="tight")
    plt.show()


# ---------- Step 5: Show Images from Each Cluster ----------
def show_cluster_images(folder, filenames, labels, max_images=10):
    clusters = {}
    for fname, label in zip(filenames, labels):
        clusters.setdefault(label, []).append(fname)

    for cluster_id, img_list in clusters.items():
        print(f"\nCluster {cluster_id}:")
        plt.figure(figsize=(15, 5))
        for i, fname in enumerate(img_list[:max_images]):
            img = mpimg.imread(os.path.join(folder, fname))
            plt.subplot(1, min(max_images, len(img_list)), i + 1)
            plt.imshow(img)
            plt.axis("off")
        plt.savefig(f"cluster_{cluster_id}.png", dpi=300, bbox_inches="tight")
        plt.show()


# ---------- Step 6: Save Clustered Images ----------
def save_clusters(folder, filenames, labels, output_dir="clusters"):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for fname, label in zip(filenames, labels):
        cluster_folder = os.path.join(output_dir, f"cluster_{label}")
        os.makedirs(cluster_folder, exist_ok=True)
        src = os.path.join(folder, fname)
        dst = os.path.join(cluster_folder, fname)
        shutil.copy(src, dst)
    print(f"✅ Images saved into '{output_dir}/cluster_x/' folders.")


# ---------- Main ----------
def main():
    folder = "./initial_images"  

    print("🔹 Loading model...")
    model = load_model()

    print("🔹 Extracting features...")
    features, filenames = extract_features(folder, model)

    print("🔹 Finding optimal k with elbow method...")
    elbow_method(features, max_k=100)

    # Choose k (adjust after elbow plot)
    n_clusters = 10
    print(f"🔹 Clustering into {n_clusters} clusters...")
    labels = cluster_features(features, n_clusters=n_clusters)

    print("🔹 Visualizing clusters with t-SNE...")
    visualize_tsne(features, labels)

    print("🔹 Showing cluster images...")
    show_cluster_images(folder, filenames, labels)

    print("🔹 Saving clustered images...")
    save_clusters(folder, filenames, labels)


if __name__ == "__main__":
    main()
