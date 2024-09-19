
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense, Dropout, LSTM, Bidirectional, GRU, SpatialDropout1D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping
def model_train(df, text_column, label_column, model_type='cnn'):
    encoder = LabelEncoder()
    df[label_column] = encoder.fit_transform(df[label_column])
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(df[text_column])
    sequences = tokenizer.texts_to_sequences(df[text_column])
    max_length = max([len(x) for x in sequences])
    X = pad_sequences(sequences, maxlen=max_length, padding='post')
    y = df[label_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    vocab_size = len(tokenizer.word_index) + 1
    embedding_dim = 256
    # Define the model
    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length))
    if model_type == 'cnn':
        model.add(Conv1D(256, 5, activation='relu'))
        model.add(Conv1D(128, 3, activation='relu'))  # Additional Conv layer
        model.add(GlobalMaxPooling1D())
    
    elif model_type == 'bilstm':
        model.add(Bidirectional(LSTM(128, return_sequences=True)))
        model.add(Bidirectional(LSTM(64, return_sequences=True)))  # Additional LSTM layer
        model.add(GlobalMaxPooling1D())
    
    elif model_type == 'gru':
        model.add(GRU(128, return_sequences=True))
        model.add(GRU(64, return_sequences=True))  # Additional GRU layer
        model.add(GlobalMaxPooling1D())

    elif model_type == 'cnn_lstm':
        model.add(Conv1D(256, 5, activation='relu'))
        model.add(SpatialDropout1D(0.2))
        model.add(Conv1D(128, 3, activation='relu'))  # Additional Conv layer
        model.add(LSTM(128, return_sequences=True))
        model.add(LSTM(64))  # Additional LSTM layer
    
    # Dense Layers (fully connected layers)
    model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.001)))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))  # Additional Dense layer
    model.add(Dropout(0.3))  # Additional Dropout layer
    model.add(Dense(32, activation='relu'))  # Additional Dense layer

    model.add(Dense(len(y.unique()), activation='softmax'))
    optimizer = Adam(learning_rate=0.001)

    #early_stopping = EarlyStopping(monitor='val_loss', patience=3)
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=25, validation_data=(X_test, y_test), batch_size=32)
    #model.fit(X_train, y_train, epochs=25, validation_data=(X_test, y_test), callbacks=[early_stopping])

    return model, tokenizer, encoder, X_test, y_test, max_length


# Example usage:
# To train the original CNN model
# model, tokenizer, encoder, X_test, y_test, max_length = model_train(df, 'text', 'label', model_type='cnn')

# To train the Bidirectional LSTM model
# model, tokenizer, encoder, X_test, y_test, max_length = model_train(df, 'text', 'label', model_type='bilstm')

# To train the GRU model
# model, tokenizer, encoder, X_test, y_test, max_length = model_train(df, 'text', 'label', model_type='gru')

# To train the CNN-LSTM hybrid model
# model, tokenizer, encoder, X_test, y_test, max_length = model_train(df, 'text', 'label', model_type='cnn_lstm')
