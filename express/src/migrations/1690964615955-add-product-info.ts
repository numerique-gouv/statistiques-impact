import { MigrationInterface, QueryRunner } from 'typeorm';

export class AddProductInfo1690964615955 implements MigrationInterface {
    name = 'AddProductInfo1690964615955';

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(
            `CREATE TABLE "product_info" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "nom_service_public_numerique" character varying NOT NULL, "metabaseVersion" character varying NOT NULL, CONSTRAINT "PK_ad6df2f64860f13fcf2cbe38dc6" PRIMARY KEY ("id"))`,
        );
        await queryRunner.query(`DROP TABLE "product"`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`DROP TABLE "product_info"`);
        await queryRunner.query(
            `CREATE TABLE "product" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "name" character varying NOT NULL, CONSTRAINT "PK_bebc9158e480b949565b4dc7a82" PRIMARY KEY ("id"))`,
        );
        await queryRunner.query(
            `ALTER TABLE "product" ADD CONSTRAINT "UQ_22cc43e9a74d7498546e9a63e77" UNIQUE ("name")`,
        );
    }
}
