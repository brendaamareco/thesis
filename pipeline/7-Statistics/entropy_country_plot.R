library(ggplot2)
library(data.table)

df <- fread("../0-Data/1_intermediate_generated_data/annotated_ranking_dataset.csv")

# Calculate medians for each country
median_values <- df[, .(median_entropy = median(entropy)), by = country]

# Create the plot
p <- ggplot(df, aes(country, entropy)) +
  geom_boxplot() +
  geom_text(data = median_values, aes(x = country, y = median_entropy,
                                       label = round(median_entropy, 2)),
            position = position_dodge(width = 0.75), vjust = -0.5) 
            
  ggsave("entropy_country_plot.png")

print(p) 


