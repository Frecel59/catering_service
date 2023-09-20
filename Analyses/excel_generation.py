# Importation des bibliothèques nécessaires
import io
import pandas as pd




def generate_excel_report(result_df, start_date, end_date):
    # Créer un objet BytesIO pour stocker les données Excel
    output = io.BytesIO()

    # Multipliez par 100 pour obtenir la représentation en pourcentage correcte
    result_df['%'] /= 100

    # Utiliser Pandas pour sauvegarder le DataFrame au format Excel
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        result_df.to_excel(writer, sheet_name='Sheet1', index=False)

        # Accédez à la feuille Excel générée pour formater les colonnes
        worksheet = writer.sheets['Sheet1']

        # Supprimer l'affichage du quadrillage
        worksheet.hide_gridlines(2)


        # Créer un format personnalisé pour les en-têtes de colonnes
        header_format = writer.book.add_format({
            'bold': True,         # En gras
            'text_wrap': True,    # Saut de ligne auto pour les en-têtes longs
            'align': 'center',    # Alignement au centre
            'valign': 'vcenter',  # Alignement vertical au centre
            'fg_color': 'red',  # Couleur de fond
            'border': 1,          # Bordures
            'font_size': 12       # Taille de police
            'font_color': 'white'
        })

        # Appliquer le format aux en-têtes de colonnes
        for col_num, value in enumerate(result_df.columns.values):
            worksheet.write(0, col_num, value, header_format)

        # Créez un format personnalisé pour la colonne A (Type)
        custom_number_format_A = writer.book.add_format({
            'font_size': 11,  # Taille de police
            'bold': True  # Police en gras
        })

        # Appliquer le format correspondant
        worksheet.set_column('A:A', len('Type') + 4, custom_number_format_A)


        # Créez un format personnalisé pour la colonne B (Nbr Couverts)
        custom_number_format_B = writer.book.add_format({
            'num_format': '#,##0',  # Format nombre avec séparateur de milliers
            'font_size': 11
        })

        # Appliquer le format correspondant
        worksheet.set_column('B:B', len('Nbr Couverts') + 2, \
            custom_number_format_B)

        # Créez un format personnalisé pour la colonne C (%)
        custom_percent_format_C = writer.book.add_format({
            'num_format': '0.00%',  # Format % avec 2 décimales
            'font_size': 11
        })

        # Appliquer le format correspondant
        worksheet.set_column('C:C', len('%') + 10, custom_percent_format_C)

        # Créez un format personnalisé pour la colonne D (Total Additions €)
        custom_compte_format_D = writer.book.add_format({
            'num_format': '#,##0.00 €',  # Format comptabilité 2 déc. + €
            'font_size': 11
        })

        # Appliquer le format correspondant
        worksheet.set_column('D:D', len('Total Additions €') + 2, \
            custom_compte_format_D)

        # Créez un format personnalisé pour la colonne E (Panier moyen €)
        custom_compte_format_E = writer.book.add_format({
            'num_format': '#,##0.00 €',
            'font_size': 11
        })

        # Appliquer le format correspondant
        worksheet.set_column('E:E', len('Panier moyen €') + 2, \
            custom_compte_format_E)


    # Définir le point de départ pour la lecture
    output.seek(0)

    return output
