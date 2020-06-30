library(googlesheets4)
library(googledrive)
library(data.table)
library(ggplot2)
library(ggthemes)
library(fuzzywuzzyR)
library(stringr)
library(stringi)
library(plyr)
options(stringsAsFactors = F)
setwd('~/repository//TriviaNight/')
sheet_results <- drive_find(type = "spreadsheet")
#sheet lookups by name
ids <- vector('list')
responses <- vector('list')
responses_melted  <- vector('list')
graded_responses <- vector('list')
ids[[1]] <- sheet_results[which(sheet_results$name == "Trivia June 2020 (Responses)"),]$id
ids[[2]] <- sheet_results[which(sheet_results$name == "Trivia - Round 2 (Responses)"),]$id
ids[[3]] <- sheet_results[which(sheet_results$name == "Trivia June 2020 - Round 3 (Responses)"),]$id
ids[[4]] <- sheet_results[which(sheet_results$name == "Trivia June 2020 - Round 4 (Responses)"),]$id
id_answers <- sheet_results[which(sheet_results$name == "Trivia June 2020 - Answers"),]$id

answers_master <- setDT(read_sheet(id_answers))
answers_master$Round <- as.character(unlist(answers_master$Round))
answers <- vector('list')
#initiate answer list
for (i in 1:4){
  answers[[i]] <- answers_master[Round == i]
}

#function to get responses for round 1 at a time
getResponses <- function(round_num){
  responses_df <- setDT(read_sheet(ids[[round_num]]))
  #each round has this question hard coded in - shortening column name for R
  names(responses_df) <- mapvalues(names(responses_df), 
    from = "What is your team name?", to = "Name")
  #get rid of the timestamp
  responses_df <- responses_df[,-c('Timestamp')]
  return(responses_df)
}


responses[[1]] <- getResponses(1)

formatForAnswers <- function(responses_df){
  responses.m  <- melt(responses_df, id = 'Name', variable.name = 'Question', value.name = 'Answer')
  #extract number from the question string
  responses.m$Number <- as.numeric(unlist(
    lapply(
      str_split(string = responses.m$Question, pattern = '\\.'), function(x) x[1]))
  )
  #initiate T/F column
  responses.m$Correct <- logical(length = nrow(responses.m))
  responses.m$Question <- factor(responses.m$Question, 
                             levels = unique(responses.m$Question))
  return (responses.m)
}
#reshaping data and dropping timestamp column so that we can add a new Graded column

responses_melted[[1]] <- formatForAnswers(responses[[1]])

gradeResponses <- function(round_num, melted_response){
  num_questions <- max(answers[[round_num]]$Number)
  for (i in 1:num_questions){
    for (team_name in unique(melted_response$Name)){
      corrects <- GetCloseMatches(answers[[round_num]]$Answer[i], melted_response[Number == i]$Answer)
      #additionally, if the answer is not a close match but is contained within the true answer, it should count
      additional <- unique(grep(answers[[round_num]]$Answer[i], melted_response[Number == i]$Answer, 
                                value=T, ignore.case = T))
      for (answer in melted_response[Number == i]$Answer){
        #grepl should work, unless answer is NA. The %in% deals with NA answers
        if (grepl(answer, answers[[round_num]]$Answer[i]) %in% T) { 
          additional <- append(additional, answer)
        }
      }
      corrects <- unique(c(corrects, additional))
      #assign true or false to each question
      melted_response[Number == i]$Correct <- melted_response[Number == i]$Answer %in% corrects
    }
  }
  #this section is entirely for plotting aesthetics
  #break questions into multiple lines for readability in graph
  str_len <- 40
  melted_response$Question_Formatted <- character(length = nrow(melted_response))
  for (i in 1:nrow(melted_response)){
    melted_response$Question_Formatted[i] <- paste(stri_wrap(melted_response$Question[i], width=str_len), collapse='\n')
  }
  melted_response$Question_Formatted <- factor(melted_response$Question_Formatted,
                                                     levels = rev(unique(melted_response$Question_Formatted)))
  #add round number also for plotting
  melted_response$Round <- round_num
  return(melted_response)
}

graded_responses[[1]] <- gradeResponses(1, responses_melted[[1]])

#plot function
plot_graded_answers <- function(graded_df, round_num, save = T){
  p <- ggplot(graded_df) + 
    geom_tile(aes(x=Name, y=Question_Formatted, fill=Correct), color='black', alpha=0.7) +
    geom_text(aes(x=Name, y=Question_Formatted, label = Answer)) +
    scale_fill_brewer(palette = 'Set1') +
    ylab('Question') +
    ggtitle(paste0('Responses - Round ', round_num)) +
    theme(plot.title = element_text(hjust=0.5), panel.background = element_blank())
  print(p)
  if (save){
    ggsave(paste0('Responses_Round', round_num, '.jpeg'), width= 18, height=9)
  }
}
#plot
plot_graded_answers(graded_responses[[1]], 1)

#helper function to quickly change an answer that wasn't graded correctly
changeGrading <- function(graded_df, team, number){
  graded_df[Name == team & Number == number]$Correct <- !graded_df[Name == team & Number == number]$Correct
  return (graded_df)
}


#sample workflow afer responses are in
n <- 4
responses[[n]] <- getResponses(n)
responses_melted[[n]] <- formatForAnswers(responses[[n]])
graded_responses[[n]] <- gradeResponses(n, responses_melted[[n]])
plot_graded_answers(graded_responses[[n]], n)

graded_responses[[1]] <- changeGrading(graded_responses[[1]], team = 'nerd immunity', number = 1)
graded_responses[[1]] <- changeGrading(graded_responses[[1]], team = 'Calenteam', number = 5)
graded_responses[[1]] <- changeGrading(graded_responses[[1]], team = 'CAL機', number = 5)
graded_responses[[1]] <- changeGrading(graded_responses[[1]], team = 'Quarantina Aguilera', number = 8)
graded_responses[[1]] <- changeGrading(graded_responses[[1]], team = 'Quarantina Aguilera', number = 10)
graded_responses[[1]] <- changeGrading(graded_responses[[1]], team = 'Quarantina Aguilera', number = 2)
graded_responses[[1]] <- changeGrading(graded_responses[[1]], team = 'nerd immunity', number = 2)
graded_responses[[1]] <- changeGrading(graded_responses[[1]], team = 'CAL機', number = 2)

graded_responses[[3]] <- changeGrading(graded_responses[[3]], team = 'HydroxyCALoquine', number = 4)
graded_responses[[3]] <- changeGrading(graded_responses[[3]], team = 'nerd immunity', number = 4)
graded_responses[[3]] <- changeGrading(graded_responses[[3]], team = 'Quarantina Aguilera', number = 3)
graded_responses[[3]] <- changeGrading(graded_responses[[3]], team = 'nerd immunity', number = 8)


graded_responses[[4]] <- changeGrading(graded_responses[[4]], team = 'nerd immunity', number = 8)

scored_list = vector('list')
for (i in 1:4){
  scored_list[[i]] <- graded_responses[[i]][, .(scores = sum(as.numeric(Correct))), by = Name]
  scored_list[[i]]$Round <- i
}


#the interlude format doesn't really fit in the same, so I'll write in manually
graded_responses[['Interlude']] <- data.frame(Name = c('Quarantina Aguilera', 'HydroxyCALoquine', 'CAL機', 'nerd immunity',
                                                       'Harem', 'Calenteam'),
                 Number = c(2, 2, 1, 1, 3, 2),
                 Answer = c('James Baldwin', 'James Baldwin', 'James Baldwin', 'James Baldwin', 'James Baldwin', 'James Baldwin'),
                 #Correct = c(T, T, T, T, T, T),
                 Correct = c(8, 8, 10, 10, 6, 8),
                 Round = rep('Interlude', 6) )
graded_responses[['Interlude']] <- setDT(graded_responses[['Interlude']])
scored_list[['Interlude']] <- graded_responses[['Interlude']][, .(scores = sum(Correct)), by = Name]
all_scores <- do.call('rbind.fill', scored_list)
setDT(all_scores)
all_answers <- do.call(rbind.fill, graded_responses)

all_scores[, .(scores = sum(scores)), by=Name]
write.csv(all_scores, 'all_scores.csv')
#finals
master <- do.call( 'rbind.fill', graded_responses)
master$Round <- as.character(master$Round)
master_merged <- merge(master, answers_master, by = c('Round', 'Number'))

master_merged <- read.csv('all_scores.csv')
setDT(master_merged)

master_merged$Round <- factor(master_merged$Round,
                              levels = c('1', '2', 'Interlude', '3', '4'))
master_merged <- master_merged[order(Round, Number)]
master_merged[, Cumulative.Score := cumsum(scores), by = list(Name)]
score_df <- master_merged[, .(scores = sum(scores)), by = 'Name']
#progression chart
master_merged$order <- paste0(master_merged$Round, ' - ', master_merged$Number)
master_merged$order <- factor(master_merged$order,
                              levels = unique(master_merged$order))


ggplot(master_merged) + 
  geom_point(aes(x=order, y=Cumulative.Score, group=Name, color=Name)) +
  geom_line(aes(x=order, y=Cumulative.Score, group=Name, color=Name)) +
  xlab('Round - Question') +
  ggtitle('Trivia Night Score Progression') +
  theme(panel.grid.minor = element_blank())

setDT(all_answers)
all_answers$Round <- factor(all_answers$Round,
                              levels = c('1', '2', 'Interlude', '3', '4'))
all_answers <- all_answers[order(Round)]
all_answers$order <- paste0(all_answers$Round, ' - ', all_answers$Number)
all_answers$order <- factor(all_answers$order,
                            levels = unique(all_answers$order))
all_answers$Point <- as.numeric(as.character((mapvalues(all_answers$Round, from = c('1', '2', '3', '4', 'Interlude'), to = c(1, 1, 2, 5, 1)))))
#assigning some half correct answers
all_answers[Round == '4' & Name == 'Quarantina Aguilera' & Number %in% c(2, 3)]$Correct <- 0.5
all_answers[Round == '4' & Name == 'Harem' & Number == 2]$Correct <- 0.5
all_answers[Round == '4' & Name == 'nerd immunity' & Number == 2]$Correct  <- 0.5

all_answers$Score <- all_answers$Correct * all_answers$Point

all_answers[, Cumulative.Score := cumsum(Score), by = list(Name)]

showtext_auto()
ggplot(all_answers[Name != 'Answers']) + 
  geom_point(aes(x=order, y=Cumulative.Score, group=Name, color=Name)) +
  geom_line(aes(x=order, y=Cumulative.Score, group=Name, color=Name)) +
  xlab('Round - Question') +
  scale_color_brewer(palette = 'Set1', 'Team Name') +
  ggtitle('Trivia Night Score Progression') +
  theme(panel.grid.minor = element_blank(),
        text = element_text(family = 'STFangsong', size=12),
        axis.text.x = element_text(angle=90))
ggsave('Score_Progression.jpeg', width= 15, height=9, dpi=150)
