install.packages("ggplot2")
install.packages("factoextra")
library(ggplot2)
library(factoextra)

data(iris)
iris_data <- iris[, -5]

iris_scaled <- scale(iris_data)

pca_result <- prcomp(iris_scaled, center = TRUE, scale. = TRUE)

fviz_eig(pca_result, addlabels = TRUE)

fviz_pca_biplot(pca_result, geom.ind = "point", pointshape = 21, 
                pointsize = 2, fill.ind = iris$Species, col.ind = "black",
                palette = "jco", addEllipses = TRUE, label = "var",
                col.var = "black", repel = TRUE)

fviz_pca_ind(pca_result, geom.ind = "point", pointshape = 21, 
             pointsize = 2, fill.ind = iris$Species, col.ind = "black",
             palette = "jco", addEllipses = TRUE, repel = TRUE)

fviz_pca_var(pca_result, col.var = "contrib", gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"), repel = TRUE)

