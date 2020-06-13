library(googlesheets4)
library(googledrive)
library(data.table)
library(ggplot2)
library(ggthemes)
library(fuzzywuzzyR)
library(stringr)
options(stringsAsFactors = F)
setwd('~/Documents/CAL/Real_Life/Blog Posts/TriviaNight/')
sheet_results <- drive_find(type = "spreadsheet")
#sheet lookups by name
ids <- vector('list')
responses <- vector('list')
responses_melted  <- vector('list')
ids[[1]] <- sheet_results[which(sheet_results$name == "Trivia June 2020 (Responses)"),]$id
ids[[2]] <- sheet_results[which(sheet_results$name == "Trivia - Round 2 (Responses)"),]$id
ids[[3]] <- sheet_results[which(sheet_results$name == "Trivia - Round 3 (Responses)"),]$id
ids[[4]] <- sheet_results[which(sheet_results$name == "Trivia June 2020 - Round 4 (Responses)"),]$id
id_answers <- sheet_results[which(sheet_results$name == "Trivia June 2020 - Answers"),]$id

answers <- setDT(read_sheet(id_answers))
#initiate answer list
for (i in 1:4){
  answers[[i]] <- answers[Round == i]
}

#function to get responses for round 1 at a time
getResponses <- function(round_num){
  responses_df <- setDT(read_sheet(ids[[round_num]]))
  #each round has this question hard coded in - shortening column name for R
  names(responses_df) <- mapvalues(names(responses_df), 
    from = "What is your team name?", to = "Name")
  return(responses_df)
}


responses[[1]] <- getResponses(1)

formatForAnswers <- function(round_num){
  responses_melted[[round_num]] <- melt(responses[[round_num]][,-1], id = 'Name', variable.name = 'Question', value.name = 'Answer')
  #extract number from the question string
  responses_melted[[round_num]]$Number <- as.numeric(unlist(
    lapply(
      str_split(string = responses_melted[[round_num]]$Question, pattern = '\\.'), function(x) x[1]))
  )
  #initiate T/F column
  responses_melted[[round_num]]$Correct <- logical(length = nrow(responses_melted[[round_num]]))
  responses_melted[[round_num]]$Question <- factor(responses_melted[[round_num]]$Question, 
                             levels = unique(responses_melted[[round_num]]$Question))
}
#reshaping data and dropping timestamp column so that we can add a new Graded column



for (i in 1:10){
  for (team_name in unique(responses_melted[[1]]$Name)){
    corrects <- GetCloseMatches(answers[[1]]$Answer[i], responses_melted[[1]][Number == i]$Answer)
    #additionally, if the answer is not a close match but is contained within the true answer, it should count
    additional <- unique(grep(answers[[1]]$Answer[i], responses_melted[[1]][Number == i]$Answer, 
                              value=T, ignore.case = T))
    for (answer in responses_melted[[1]][Number == i]$Answer){
      #grepl should work, unless answer is NA. The %in% deals with NA answers
      if (grepl(answer, answers[[1]]$Answer[i]) %in% T) { 
        additional <- append(additional, answer)
      }
    }
    corrects <- unique(c(corrects, additional))
    responses_melted[[1]][Number == i]$Correct <- responses_melted[[1]][Number == i]$Answer %in% corrects
  }
}

#break questions into multiple lines for readability in graph
str_len <- 40
responses_melted[[1]]$Question_Formatted <- character(length = nrow(responses_melted[[1]]))
for (i in 1:nrow(responses_melted[[1]])){
  responses_melted[[1]]$Question_Formatted[i] <- paste(stri_wrap(responses_melted[[1]]$Question[i], width=str_len), collapse='\n')
}
responses_melted[[1]]$Question_Formatted <- factor(responses_melted[[1]]$Question_Formatted,
                                     levels = rev(unique(responses_melted[[1]]$Question_Formatted)))
#plot
ggplot(responses_melted[[1]]) + geom_tile(aes(x=Name, y=Question_Formatted, fill=Correct), color='black') +
  geom_text(aes(x=Name, y=Question_Formatted, label = Answer)) +
  scale_fill_brewer(palette = 'Set2') +
  ylab('Question') +
  ggtitle('Responses - Round 1')
ggsave('Responses_Round1.jpeg', width= 12, height=9)

names(responses[[2]]) <- mapvalues(names(responses[[2]]), from = "What is your team name?", to = "Name")
responses[[2]].m <- melt(responses[[2]][,-1], id = 'Name', variable.name = 'Question', value.name = 'Answer')
responses[[2]].m$Number <- as.numeric(unlist(
  lapply(
    str_split(string = responses[[2]].m$Question, pattern = '\\.'), function(x) x[1])
)
)
responses[[2]].m$Correct <- logical()
answers2 <- answers[Round == 2]
for (i in 1:10){
  corrects <- GetCloseMatches(answers2[Number == i]$Answer, responses[[2]].m[Number == i]$Answer)
  responses[[2]].m[Number == i]$Correct <- responses[[2]].m[Number == i]$Answer %in% corrects
}






