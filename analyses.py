import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from tabulate import tabulate
import matplotlib.pyplot as plt
from Data_cleaning.df_global import merged_df


def main():
    st.title("Analyses")
    st.write("")

    # Appeler la fonction merged_df pour obtenir les données avec météo
    df_final = merged_df()



    # Créer une mise en page en colonnes
    col1, col2 = st.columns(2)

    # Ajouter le widget date_input dans la première colonne
    with col1:
        # start_date = st.date_input("Date de départ", df_final["Date"].max() - pd.DateOffset(months=1), key="start_date_input") # mois précédent de date max
        start_date = st.date_input("Date de départ", datetime((df_final["Date"].max()).year - 1, 11, 1), key="start_date_input") # 01/11 + année -1 de date max

    with col2:
        end_date = st.date_input("Date de fin", df_final["Date"].max(), key="end_date_input")

    # Convertir les dates sélectionnées en objets datetime64[ns]
    start_date_convert = pd.to_datetime(start_date)
    end_date_convert = pd.to_datetime(end_date)

    # Filtrer le DataFrame en fonction des dates choisies
    filtered_df = df_final[(df_final["Date"] >= start_date_convert) & (df_final["Date"] <= end_date_convert)]

    #########################################################################
    # CALCUL SUR LE DATAFRAME

    columns_to_sum = ['Nbr couv. 19h', 'Additions 19h', 'Nbr couv. off 19h', 'Additions off 19h', 'Nbr couv 12h', 'Additions 12h', 'Nbr couv. off 12h', 'Additions off 12h']
    sums = filtered_df[columns_to_sum].sum()

    # Sommes des covers et des prices
    total_Covers_sales = sums['Nbr couv. 19h'] + sums['Nbr couv 12h']
    total_Price_sales = sums['Additions 19h'] + sums['Additions 12h']
    total_Covers_intern = sums['Nbr couv. off 19h'] + sums['Nbr couv. off 12h']
    total_Price_intern = sums['Additions off 19h'] + sums['Additions off 12h']
    total_Covers = total_Covers_sales + total_Covers_intern

    # Pourcentage des covers et des prices
    percentage_Covers_sales = (total_Covers_sales / total_Covers) * 100
    percentage_Covers_intern = (total_Covers_intern / total_Covers) * 100

    # Panier moyen
    panier_sales = total_Price_sales / total_Covers_sales
    panier_intern = total_Price_intern / total_Covers_intern
    panier_total = total_Price_sales / total_Covers

    # Créer une liste de tuples pour chaque ligne du tableau
    # Formater les valeurs dans la colonne "Nbr Couverts" sans décimales et avec un espace comme séparateur de milliers
    total_Covers_sales_formatted = f"{int(total_Covers_sales):,}".replace(",", " ")
    total_Covers_intern_formatted = f"{int(total_Covers_intern):,}".replace(",", " ")
    total_Covers_formatted = f"{int(total_Covers):,}".replace(",", " ")

    table_data_global = [
        ("Payants", total_Covers_sales_formatted, f"{percentage_Covers_sales:.2f} %", f"{total_Price_sales:,.2f} €", f"{panier_sales:,.2f} €"),
        ("Offerts", total_Covers_intern_formatted, f"{percentage_Covers_intern:.2f}%", f"{total_Price_intern:,.2f} €", f"{panier_intern:,.2f} €"),
        ("Réalisés", total_Covers_formatted, "100 %", f"{total_Price_sales:,.2f} €", f"{panier_total:,.2f} €"),
    ]




    #########################################################################
    # AFFICHAGE DES DONNEES SOUHAITEES SUR L'APP

    # Insérer un séparateur horizontal avec style CSS personnalisé
    st.markdown('<hr style="border: 2px solid red;">', unsafe_allow_html=True)

    # Afficher le tableau formaté
    # Formater les dates au format "dd-mm-yyyy"
    formatted_start_date = start_date.strftime("%d-%m-%Y")
    formatted_end_date = end_date.strftime("%d-%m-%Y")

    st.write("")
    st.write(f"Période : du {formatted_start_date} au {formatted_end_date}")
    formatted_table = tabulate(table_data_global, headers=["Type", "Nbr Couverts", "%", "Total", "Panier moyen"], tablefmt="fancy_grid")
    st.text(formatted_table)

    # Insérer un séparateur horizontal avec style CSS personnalisé
    st.markdown('<hr style="border: 2px solid red;">', unsafe_allow_html=True)


 #########################################################################
   # GRAPHIQUE AVEC WIDGETS STREAMLIT
    # Convertir la colonne 'date' en datetime
    filtered_df['date'] = pd.to_datetime(filtered_df['Date'])

    # Créer les widgets
    # Créer une mise en page en colonnes
    col1, col2, col3 = st.columns(3)

    # Ajouter le widget date_input dans la première colonne
    with col1:
        group_by_option = st.selectbox('Trier par :', ['Jour', 'Mois et Jour'])

    with col2:
        data_type_option = st.selectbox('Type de données :', ['Nbr total couv. 12h', 'Nbr total couv. 19h', 'Nbr total couv.', 'Additions 12h', 'Additions 19h', 'Total additions'])


    if group_by_option == 'Mois et Jour':
        unique_months = filtered_df['date'].dt.to_period("M").unique().strftime('%Y-%m').tolist()
        with col3:
            month_option = st.selectbox('Mois :', unique_months)
        # month_option = st.selectbox('Mois :', unique_months)
    else:
        month_option = None

    # Fonction pour afficher le graphique
    def show_grouped_data(group_by, data_type, month):
        days_order = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

        df_grouped = filtered_df.copy()
        if group_by == 'Jour':
            df_grouped['Jour'] = pd.Categorical(df_grouped['Jour'], categories=days_order, ordered=True)
            grouped = df_grouped.groupby('Jour')[data_type].sum().reset_index()

        elif group_by == 'Mois et Jour' and month:
            df_grouped['mois'] = df_grouped['date'].dt.to_period("M")
            df_grouped['Jour'] = pd.Categorical(df_grouped['Jour'], categories=days_order, ordered=True)
            grouped = df_grouped[df_grouped['mois'].dt.strftime('%Y-%m') == month].groupby(['mois', 'Jour'])[data_type].sum().reset_index()

        fig, ax = plt.subplots()
        ax.bar(grouped['Jour'], grouped[data_type])
        ax.set_xlabel(group_by)
        ax.set_ylabel(data_type)
        ax.set_title(f"Répartition par {group_by_option} pour {data_type_option}")
        ax.set_xticklabels(grouped['Jour'], rotation=45)
        st.pyplot(fig)

    # Afficher le graphique en fonction des widgets
    show_grouped_data(group_by_option, data_type_option, month_option)


    ####################################################################
    # Insérer un séparateur horizontal avec style CSS personnalisé
    st.markdown('<hr style="border: 2px solid red;">', unsafe_allow_html=True)

    # Afficher le Dataframe filtré
    st.write("Données avec météo pour la période sélectionnée :")
    st.dataframe(filtered_df)





if __name__ == "__main__":
    main()
