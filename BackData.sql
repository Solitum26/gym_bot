PGDMP     :    
                {            BackData    15.2    15.2     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16399    BackData    DATABASE     �   CREATE DATABASE "BackData" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_United States.1252';
    DROP DATABASE "BackData";
                postgres    false            �           0    0    DATABASE "BackData"    COMMENT     9   COMMENT ON DATABASE "BackData" IS 'Back exercises data';
                   postgres    false    3320            �            1259    24576    exercises_data    TABLE     w   CREATE TABLE public.exercises_data (
    user_id integer,
    date date,
    exercise text,
    train_params text[]
);
 "   DROP TABLE public.exercises_data;
       public         heap    postgres    false            �          0    24576    exercises_data 
   TABLE DATA           O   COPY public.exercises_data (user_id, date, exercise, train_params) FROM stdin;
    public          postgres    false    214          �   f   x��K
�  �z?�y���DѮ֝C�~X��y�l33�X�tY���\h����C���aCLCn'"�4�#�%ی;���t��R�L��aM�˞���E/�     