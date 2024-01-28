library(ggplot2)

df <- fread("computational_complexity.csv")
df$Combinaciones <- as.integer(df$Combinaciones)


# Create the plot
p <- ggplot(df, aes(x = Precision, y = Combinaciones)) +
  geom_point() +
  stat_smooth(method = loess)  
            
  ggsave("plot.png")

print(p) 


