#!/usr/bin/python
# -*- coding: utf-8 -*-

from Service.Enum.Status import Status
from aqt.utils import showInfo

from typing import List

from ...Ui.UiAnkiFlash import UiAnkiFlash
from ...Service.Enum.Translation import Translation
from ...Service.Enum.Card import Card
from ...Service.BaseGenerator import BaseGenerator
from ...Service.Constant import Constant
from ...Helpers.HtmlHelper import HtmlHelper
from ...Helpers.DictHelper import DictHelper


class EnglishGenerator(BaseGenerator):

    def getFormattedWords(self, word: str, translation: Translation) -> List[str]:
        word = word.lower()
        foundWords = []
        if (translation.equals(Constant.EN_EN)):
            foundWords.addAll(DictHelper.getOxfordWords(word))
        else:
            foundWords.add(word + Constant.SUB_DELIMITER +
                           word + Constant.SUB_DELIMITER + word)
        return foundWords

    def generateCard(self, ui: UiAnkiFlash, formattedWord: str, translation: Translation, isOnline: bool) -> Card:
        
        formattedWord = formattedWord.toLowerCase()
        card = Card()
        wordParts: list[str] = formattedWord.split(Constant.SUB_DELIMITER)
        if Constant.SUB_DELIMITER in formattedWord and len(wordParts) == 3:
            card = Card(wordParts[0], wordParts[1], wordParts[2], translation.toString())
        else:
            card.status = Status.Word_Not_Found
            card.comment = "Incorrect word format=".format(formattedWord)
            return card
        

        logging.info("Word = {}", card.getWord());
        logger.info("WordId = {}", card.getWordId());
        logger.info("OriginalWord = {}", card.getOriginalWord());

        logger.info("Source = {}", translation.getSource());
        logger.info("Target = {}", translation.getTarget());

        DictionaryContentService oxfordDict = new OxfordDictionaryContentServiceImpl();
        DictionaryContentService cambridgeDict = new CambridgeDictionaryContentServiceImpl();
        DictionaryContentService lacVietDict = new LacVietDictionaryContentServiceImpl();

        String hashCombination = formattedWord + Constant.SUB_DELIMITER + translation.toString();
        logger.info("Finding-hash-combination={}", hashCombination);
        Card dbCard = cardStorageService.findByHash(card.getHash());
        if (dbCard != null) {
        logger.info("Card-found-from-our-DB={}", card.getWord());
        if (isOffline) {
            DictHelper.downloadFiles(ankiDir, dbCard.getImageLink());
            DictHelper.downloadFiles(ankiDir, dbCard.getSoundLink());
        }
        return dbCard;
        }

        // English to English
        if (translation.equals(Translation.EN_EN)) {
        if (oxfordDict.isConnected(formattedWord, translation)) {
            card.setStatus(Status.Connection_Failed);
            card.setComment(Constant.CONNECTION_FAILED);
            return card;
        } else if (oxfordDict.isInvalidWord()) {
            card.setStatus(Status.Word_Not_Found);
            card.setComment(Constant.WORD_NOT_FOUND);
            return card;
        }

        card.setWordType(oxfordDict.getWordType());
        card.setPhonetic(oxfordDict.getPhonetic());
        card.setMeaning(oxfordDict.getMeaning());
        card.setCopyright(String.format(Constant.COPYRIGHT, oxfordDict.getDictionaryName()));

        // English to Chinese/French/Japanese
        } else if (translation.equals(Translation.EN_CN_TD)
            || translation.equals(Translation.EN_CN_SP)
            || translation.equals(Translation.EN_JP)
            || translation.equals(Translation.EN_FR)) {

        if (oxfordDict.isConnected(formattedWord, translation)
            || cambridgeDict.isConnected(formattedWord, translation)) {
            card.setStatus(Status.Connection_Failed);
            card.setComment(Constant.CONNECTION_FAILED);
            return card;
        } else if (oxfordDict.isInvalidWord() || cambridgeDict.isInvalidWord()) {
            card.setStatus(Status.Word_Not_Found);
            card.setComment(Constant.WORD_NOT_FOUND);
            return card;
        }

        card.setWordType(oxfordDict.getWordType());
        card.setPhonetic(oxfordDict.getPhonetic());
        card.setMeaning(cambridgeDict.getMeaning());
        card.setCopyright(
            String.format(
                Constant.COPYRIGHT,
                String.join(
                    ", and ", oxfordDict.getDictionaryName(), cambridgeDict.getDictionaryName())));

        // English to Vietnamese
        } else if (translation.equals(Translation.EN_VN)) {

        if (oxfordDict.isConnected(formattedWord, translation)
            || lacVietDict.isConnected(formattedWord, translation)) {
            card.setStatus(Status.Connection_Failed);
            card.setComment(Constant.CONNECTION_FAILED);
            return card;
        } else if (oxfordDict.isInvalidWord() || lacVietDict.isInvalidWord()) {
            card.setStatus(Status.Word_Not_Found);
            card.setComment(Constant.WORD_NOT_FOUND);
            return card;
        }

        card.setWordType(oxfordDict.getWordType());
        card.setPhonetic(oxfordDict.getPhonetic());
        card.setMeaning(lacVietDict.getMeaning());
        card.setCopyright(
            String.format(
                Constant.COPYRIGHT,
                String.join(
                    ", and ", oxfordDict.getDictionaryName(), lacVietDict.getDictionaryName())));

        } else {
        card.setStatus(Status.Not_Supported_Translation);
        card.setComment(
            String.format(
                Constant.NOT_SUPPORTED_TRANSLATION,
                translation.getSource(),
                translation.getTarget()));
        return card;
        }

        oxfordDict.getSounds(ankiDir, isOffline);
        card.setSoundOnline(oxfordDict.getSoundOnline());
        card.setSoundOffline(oxfordDict.getSoundOffline());
        card.setSoundLink(oxfordDict.getSoundLinks());

        oxfordDict.getImages(ankiDir, isOffline);
        card.setImageOffline(oxfordDict.getImageOffline());
        card.setImageOnline(oxfordDict.getImageOnline());
        card.setImageLink(oxfordDict.getImageLink());

        card.setExample(oxfordDict.getExample());
        card.setTag(oxfordDict.getTag());
        card.setStatus(Status.Success);
        card.setComment(Constant.SUCCESS);

        if (card.getStatus().compareTo(Status.Success) == 0
            && cardStorageService.findByHash(card.getHash()) == null
            && !ankiDir.isEmpty()) {
        logger.info("Card-created-successfully-adding-to-DB: {}", card.getWord());
        cardStorageService.save(card);
        }

        return card;
        return Card()
