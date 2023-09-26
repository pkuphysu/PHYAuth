IMAGE_NAME=registry.phy.np.mk/phy/auth
IMAGE_TAG=v1.0.0

docker:
	docker buildx build --platform=linux/amd64,linux/arm64 -t $(IMAGE_NAME):$(IMAGE_TAG) . --push